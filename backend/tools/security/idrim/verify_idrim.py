# backend/tools/security/idrim/verify_idrim.py

    IDRIMEngine,
    IDRIMService,
    IDRIMRequest,
)


def main():
    print("[IDRIM] Starting verification...")

    # Instantiate engine
    engine = IDRIMEngine()
    print("[IDRIM] Engine:", type(engine).__name__)

    # Instantiate service
    service = IDRIMService()
    print("[IDRIM] Service:", type(service).__name__)

    # Build a minimal request
    payload = {
        "source": "verification",
        "scope": "smoke",
        "payload": {
            "roles": {},
            "permissions": {},
            "users": {},
        },
    }

    req = IDRIMRequest(**payload)
    print("[IDRIM] Request:", req)

    # Pass a dict to the engine
    snapshot_dict = req.payload

    # Run analysis
    result = engine.analyze(snapshot_dict)

    # result is a dict, so use dict access
    print("[IDRIM] Engine Analysis OK:", result["summary"])

    print("[IDRIM] Verification complete.")


if __name__ == "__main__":
    main()
