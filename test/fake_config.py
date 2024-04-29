class FakeAuthCfg:
    secret = "fake-jwt-secret"
    alg = "HS256"

class FakeAWSCfg:
    host = "http://localhost:123"
    region = "us-east-1"
    access_key_id = "fake-key"
    secret_access_key = "fake-secret"

class FakeImageServiceCfg:
    max_image_size_mb = 1
    allowed_extensions = ["jpeg"]
