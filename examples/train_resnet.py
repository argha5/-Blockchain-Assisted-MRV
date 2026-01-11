"""
Example: Training ResNet18 on CIFAR-10 with MRV Tracking

This example demonstrates how to integrate the MRV wrapper into
a PyTorch training workflow.
"""

import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader

# Import MRV wrapper
from mrv_wrapper import MRVTracker


def create_model():
    """Create ResNet18 model."""
    model = torchvision.models.resnet18(pretrained=False, num_classes=10)
    return model


def train_epoch(model, train_loader, criterion, optimizer, device):
    """Train for one epoch."""
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    for batch_idx, (inputs, targets) in enumerate(train_loader):
        inputs, targets = inputs.to(device), targets.to(device)
        
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
        _, predicted = outputs.max(1)
        total += targets.size(0)
        correct += predicted.eq(targets).sum().item()
        
        if batch_idx % 100 == 99:
            print(f'  Batch {batch_idx+1}: Loss: {running_loss/(batch_idx+1):.3f} | Acc: {100.*correct/total:.2f}%')
    
    return running_loss / len(train_loader), 100. * correct / total


def test(model, test_loader, criterion, device):
    """Test the model."""
    model.eval()
    test_loss = 0
    correct = 0
    total = 0
    
    with torch.no_grad():
        for inputs, targets in test_loader:
            inputs, targets = inputs.to(device), targets.to(device)
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            
            test_loss += loss.item()
            _, predicted = outputs.max(1)
            total += targets.size(0)
            correct += predicted.eq(targets).sum().item()
    
    return test_loss / len(test_loader), 100. * correct / total


def main():
    # Configuration
    batch_size = 128
    epochs = 5  # Reduced for demo purposes (normally 90)
    learning_rate = 0.1
    
    # Device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    # Data preparation
    print("Preparing CIFAR-10 dataset...")
    transform_train = transforms.Compose([
        transforms.RandomCrop(32, padding=4),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010))
    ])
    
    transform_test = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010))
    ])
    
    trainset = torchvision.datasets.CIFAR10(
        root='./data', train=True, download=True, transform=transform_train
    )
    train_loader = DataLoader(trainset, batch_size=batch_size, shuffle=True, num_workers=2)
    
    testset = torchvision.datasets.CIFAR10(
        root='./data', train=False, download=True, transform=transform_test
    )
    test_loader = DataLoader(testset, batch_size=batch_size, shuffle=False, num_workers=2)
    
    # Create model
    model = create_model().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=learning_rate, momentum=0.9, weight_decay=5e-4)
    
    # =================================================================
    # START MRV TRACKING
    # =================================================================
    with MRVTracker(
        experiment_name="resnet18_cifar10_baseline",
        model_name="ResNet18",
        dataset_name="CIFAR-10",
        epochs=epochs,
        batch_size=batch_size,
        framework="PyTorch",
        blockchain_enabled=True,  # Enable blockchain anchoring
        auto_anchor=True  # Automatically anchor after training
    ) as tracker:
        
        print("\n" + "="*60)
        print("Starting Training with MRV Tracking")
        print("="*60 + "\n")
        
        # Training loop
        for epoch in range(epochs):
            print(f"Epoch {epoch+1}/{epochs}")
            train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, device)
            test_loss, test_acc = test(model, test_loader, criterion, device)
            
            print(f"Train Loss: {train_loss:.3f} | Train Acc: {train_acc:.2f}%")
            print(f"Test Loss: {test_loss:.3f} | Test Acc: {test_acc:.2f}%\n")
        
        # Training complete - MRV data will be automatically saved when exiting context
    
    # =================================================================
    # MRV TRACKING COMPLETE
    # =================================================================
    
    print("\n" + "="*60)
    print("Training Complete!")
    print("="*60)
    print(f"\n✅ MRV ID: {tracker.mrv_id}")
    print(f"✅ Hash: {tracker.get_hash()}")
    
    if tracker.tx_hash:
        print(f"✅ Blockchain TX: {tracker.tx_hash}")
        print("\n💡 You can now verify this MRV record on the dashboard!")
        print("   1. Start the dashboard: cd dashboard && python -m http.server 8080")
        print(f"   2. Upload: mrv_data/{tracker.mrv_id}.json")
        print(f"   3. Enter MRV ID: {tracker.mrv_id}")
    else:
        print("\n⚠️  Blockchain anchoring skipped (node not running)")
    
    print("\n📊 Include this MRV ID in your paper for verifiable sustainability claims!")


if __name__ == "__main__":
    main()
