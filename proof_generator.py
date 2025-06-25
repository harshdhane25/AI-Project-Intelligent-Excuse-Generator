import random

def generate_fake_proof(scenario):
    proofs = {
        "Work": ["proofs/proof1.jpg", "proofs/proof2.jpg"],
        "Family": ["proofs/proof3.jpg", "proofs/proof4.jpg"]
    }
    return random.choice(proofs.get(scenario, ["proofs/proof1.jpg"]))