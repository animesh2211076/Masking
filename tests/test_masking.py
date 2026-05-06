from masking import mask_user_object

def test_mask_user_object_user_role():
    user = {
        "name": "Animesh",
        "phone": "9876543210",
        "email": "animesh@gmail.com",
        "pan": "ABCDE1234F",
        "ifsc": "SBIN0001234",
        "upi": "animesh@upi",
        "account": "123456789012",
        "balance": 5400.0,
    }

    masked = mask_user_object(user, role="user")

    assert masked["email"] != "animesh@gmail.com"
    assert masked["phone"] != "9876543210"
