# ------------------------------
# Imports
# ------------------------------
import os, numpy as np
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import make_password
from .models import WasteRecord, Profile
import tensorflow as tf
from tensorflow.keras.preprocessing import image


# ------------------------------
# Load TensorFlow Lite ML Model
# ------------------------------

# Path to base directory of project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path to the quantized CNN model file
MODEL_PATH = os.path.join(BASE_DIR, "models", "waste_cnn_quant.tflite")

# Load TFLite model interpreter
interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

# Get input/output details for feeding data into model
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Class labels for predictions
CLASSES = ["Cardboard", "Compost", "E-Waste", "Glass", "Metal", "Paper", "Plastic"]

# Dictionary: maps waste type → list of possible recycled products
RECYCLE_DICT = {
    "Plastic": [
        "Bottles → Clothing fibers, carpets, ropes, insulation",
        "Containers → New packaging, storage boxes, bins, furniture",
        "Plastic bags → Composite lumber, reusable bags, mats, tiles",
        "Packaging films → Recycled sheets, floor mats, tarps, covers",
        "PET plastics → Recycled drink bottles, fibers, pillow filling, blankets"
    ],
    "Paper": [
        "Old paper → Tissue paper, notebooks, napkins, packaging paper",
        "Cardboard → New boxes, cartons, packaging boards, storage units",
        "Newspapers → Recycled newsprint, egg cartons, wrapping paper",
        "Magazines → Paperboard packaging, gift boxes, envelopes, tags",
        "Shredded paper → packing material, molded trays, seed paper"
    ],
    "Cardboard": [
        "Cartons → Recycled boxes, gift boxes, packaging boards, folders",
        "Shipping boxes → Corrugated sheets, storage bins, recycled boxes",
        "Food cartons → Compostable packaging, recycled boards, eco plates",
        "Cardboard cores → Paper tubes, rolls, craft materials, recycled boards",
        "Egg cartons → Molded packaging, trays, seedling holders, insulation"
    ],
    "Glass": [
        "Bottles → New glass bottles, jars, containers, decorative glass",
        "Jars → Fiberglass insulation, new jars, tiles, recycled containers",
        "Broken glass → Road material, cement additive, tiles, bricks",
        "Colored glass → Decorative tiles, beads, flooring, mosaics",
        "Glass sheets → Window glass, mirrors, tabletops, panels"
    ],
    "Metal": [
        "Cans → New cans, bikes, auto parts, tools",
        "Aluminum foil → Engine parts, aircraft parts, wires, utensils",
        "Steel scraps → Construction steel, bridges, pipelines, car parts",
        "Copper wires → Electrical components, motors, transformers, cables",
        "Iron scraps → Furniture, pipes, rods, building frames"
    ],
    "Compost": [
        "Food waste → Fertilizer, bio-gas, soil conditioner, bio-fuel",
        "Garden waste → Compost soil, mulch, organic fertilizer, biochar",
        "Leaves → Organic mulch, manure, compost soil, plant bedding",
        "Coffee grounds → Soil enhancer, natural pesticide, fertilizer",
        "Vegetable scraps → Organic compost, garden soil, bio-fertilizer"
    ],
    "E-Waste": [
        "Circuit boards → Extract metals (gold, silver, copper, palladium)",
        "Mobile phones → Rare earth elements, display glass, batteries",
        "Batteries → Recycled lithium, cobalt, nickel, manganese",
        "Old computers → Refurbished devices, raw materials, aluminum",
        "Wires & cables → Recovered copper, aluminum, plastics, insulation"
    ]
}


# ------------------------------
# 1. User Registration
# ------------------------------
def register(request):
    if request.method == "POST":
        # Collect form data
        first_name = request.POST.get("first_name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        dob = request.POST.get("dob")

        # Check if both passwords match
        if password != confirm_password:
            return render(request, "register.html", {"error": "Passwords do not match"})

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {"error": "Username already exists"})

        # Create new user (password is hashed before saving)
        user = User.objects.create(
            username=username,
            first_name=first_name,
            password=make_password(password),
        )

        # Create profile entry with date of birth
        Profile.objects.create(user=user, dob=dob)

        # Redirect to login page
        return redirect("login")

    # Show empty registration form if GET request
    return render(request, "register.html")


# ------------------------------
# 2. User/Admin Login
# ------------------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Special case: login as admin (username=admin, password=admin)
        if username == "admin" and password == "admin":
            user = authenticate(username="admin", password="admin")

            # If admin doesn't exist, create it
            if not user:
                user = User.objects.create_superuser(
                    username="admin", password="admin", email=""
                )
            login(request, user)
            return redirect("admin_dashboard")

        # Normal user authentication
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")   # Redirect to user home
        else:
            return render(request, "login.html", {"error": "Invalid username or password"})

    # Show login form
    return render(request, "login.html")


# ------------------------------
# 3. Logout
# ------------------------------
def logout_view(request):
    logout(request)
    return redirect("login")


# ------------------------------
# 4. User Home - Upload image & Predict
# ------------------------------
@login_required
def user_home(request):
    if request.method == "POST" and request.FILES.get("file"):
        # Save uploaded image
        upload = request.FILES["file"]
        fs = FileSystemStorage()
        saved_name = fs.save(upload.name, upload)
        saved_path = fs.path(saved_name)

        # Prepare image for model
        input_shape = input_details[0]['shape']
        target_size = (input_shape[1], input_shape[2])  # usually (224,224)

        img = image.load_img(saved_path, target_size=target_size)
        arr = image.img_to_array(img) / 255.0   # normalize values 0-1
        arr = np.expand_dims(arr, axis=0).astype(np.float32)

        # Run inference with TFLite model
        interpreter.set_tensor(input_details[0]['index'], arr)
        interpreter.invoke()
        prediction = interpreter.get_tensor(output_details[0]['index'])

        # Get predicted waste type
        waste_type = CLASSES[int(np.argmax(prediction))]

        # Save record in database
        record = WasteRecord.objects.create(user=request.user, image=upload, waste_type=waste_type)

        # Redirect to result page
        return redirect("predict_result", record_id=record.id)

    # If GET, just show upload page
    return render(request, "home.html")


# ------------------------------
# 5. Prediction Result Page
# ------------------------------
@login_required
def predict_result(request, record_id):
    # Fetch prediction record of current user
    record = WasteRecord.objects.get(id=record_id, user=request.user)

    # Get recycle products for predicted type
    products = RECYCLE_DICT.get(record.waste_type, ["No info available"])

    return render(
        request, "predict_result.html", {"record": record, "products": products}
    )


# ------------------------------
# 6. Recycle List Page
# ------------------------------
@login_required
def recycle_list(request, waste_type):
    # Fetch recycle info for given waste type
    products = RECYCLE_DICT.get(waste_type, ["No info available"])
    return render(request, "recycle.html", {
        "waste_type": waste_type,
        "products": products
    })


# ------------------------------
# 7. Admin Dashboard + Lists
# ------------------------------

# Admin dashboard page
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    return render(request, "admin_dashboard.html")

# Show all registered users
@user_passes_test(lambda u: u.is_superuser)
def user_list(request):
    users = Profile.objects.select_related("user").all()
    return render(request, "user_list.html", {"users": users})

# Show all waste prediction records
@user_passes_test(lambda u: u.is_superuser)
def waste_records(request):
    records = WasteRecord.objects.select_related("user").all()
    return render(request, "waste_records.html", {"records": records})
