"""
Simple example: MRV tracking for any Python code

This minimal example shows how to use MRV tracker with any code.
"""

from mrv_wrapper import MRVTracker
import time


def my_training_function():
    """Simulate training workload."""
    print("Training started...")
    
    # Simulate training epochs
    for epoch in range(10):
        # Simulate computation
        time.sleep(0.5)
        print(f"Epoch {epoch+1}/10 completed")
    
    print("Training completed!")


# Use MRV tracker
with MRVTracker(
    experiment_name="simple_example",
    model_name="MyModel",
    dataset_name="MyDataset",
    epochs=10,
    batch_size=32,
    framework="PyTorch"
) as tracker:
    my_training_function()

# MRV data automatically saved
print(f"\n✅ MRV ID: {tracker.mrv_id}")
print(f"✅ MRV file saved at: mrv_data/{tracker.mrv_id}.json")
