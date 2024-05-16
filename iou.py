def calculate_iou(box1, box2):
    """
    Calculate the intersection over union (IoU) between two bounding boxes.

    Args:
        box1: A tuple of integers (x1, y1, x2, y2) representing the top-left and
              bottom-right coordinates of the first bounding box.
        box2: A tuple of integers (x1, y1, x2, y2) representing the top-left and
              bottom-right coordinates of the second bounding box.

    Returns:
        A float value between 0 and 1 representing the IoU of the two bounding boxes.
    """
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    if x2 <= x1 or y2 <= y1:
        return 0.0

    intersection_area = (x2 - x1) * (y2 - y1)

    box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])

    iou = intersection_area / float(box1_area + box2_area - intersection_area)

    return iou
