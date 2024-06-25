from ImageProcessing.AbstractImageProcessing import ImageProcessing
import cv2
import torch
from torchvision import models, transforms
from torchvision.models.detection.rpn import AnchorGenerator
from PIL import Image

class LegoBrickSorting(ImageProcessing):
    def __init__ (self, model_weight_path="Path_To_Trained_Model_Weight.pth"):

        """ Off the shelve object detection model, should be fine tuned based on Lego data set
        Args:
            model_weight_path (str, optional): path of model weight
        """

        self.model = self._get_model()
        self.model_weight_path = model_weight_path
        self.model.load_state_dict(torch.load(self.model_weight_path))
        self.device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
        self.model.to(self.device)

        self.preprocess = transforms.Compose([
            transforms.ToTensor(),  # Convert NumPy array to PyTorch tensor
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),])  # Normalize as per the model's requirements

    
    def run(self, images: list) -> list:
        # convert np array to torch tensor
        input_batch = self._numpy_to_tensor(images)
        
        # run inference
        with torch.no_grad():
            result = self.model(input_batch)        
        
        return result 
            
    def _numpy_to_tensor(self, images):
        tensors = []
        for img in images:
            # Convert NumPy array to PIL image
            pil_image = Image.fromarray(img.astype('uint8'), 'RGB')
            # Preprocess the image and add batch dimension
            tensor_image = self.preprocess(pil_image).unsqueeze(0)
            tensors.append(tensor_image)
        # Concatenate all tensors to create a batch
        return torch.cat(tensors)
    
    def _get_model():
        num_classes=137  # depends on real dataset
        
        # Encoder backbone
        backbone = models.detection.backbone_utils.resnet_fpn_backbone(backbone_name="resnet50",
                                                                    pretrained=True,
                                                                    trainable_layers=0)

        anchor_sizes = ((8,), (16,), (64,), (256,), (512,))
        aspect_ratios = ((0.5, 0.8, 1.0, 1.25, 2.0),) * len(anchor_sizes)

        anchor_generator = AnchorGenerator(sizes=anchor_sizes,
                                        aspect_ratios=aspect_ratios)

        model = models.detection.FasterRCNN(backbone=backbone,
                                            num_classes=num_classes,
                                            rpn_anchor_generator=anchor_generator)

        return model


## Quick functionality test on lego brick recongition.
def test():
    brick_sorting = LegoBrickSorting()
    img = cv2.imread("PATH to Sample Testing image contains lego brick")
    result = brick_sorting.run(img)


if __name__ == "__main__":
    test()
