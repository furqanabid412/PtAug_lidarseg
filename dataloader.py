import numpy as np

from det3d.datasets.dataset_factory import get_dataset
from det3d.models import build_detector
from det3d.torchie import Config
from det3d.datasets import build_dataset

from torch.utils.data import DataLoader
from det3d.torchie.parallel import collate, collate_kitti

import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")

import cv2

import time

def example_to_device(example, device, non_blocking=False) -> dict:
    example_torch = {}
    float_names = ["voxels", "bev_map"]
    for k, v in example.items():
        if k in ["anchors", "anchors_mask", "reg_targets", "reg_weights", "labels", "hm",
                "anno_box", "ind", "mask", 'cat']:
            example_torch[k] = [res.to(device, non_blocking=non_blocking) for res in v]
        elif k in [
            "voxels",
            "bev_map",
            "coordinates",
            "num_points",
            "points",
            "num_voxels",
            "img",
            "voxels_uv",
            "voxel_valid",
            "voxels_imgfeat",
            "bev_sparse"
        ]:
            example_torch[k] = v.to(device, non_blocking=non_blocking)
        elif k == "calib":
            calib = {}
            for k1, v1 in v.items():
                calib[k1] = v1.to(device, non_blocking=non_blocking)
            example_torch[k] = calib
        else:
            example_torch[k] = v

    return example_torch


if __name__ == "__main__":
    config_file = 'E:\work\pointcloud\TestCodes\downloaded\Point_Augmenting\PointAugmenting-main\PointAugmenting-main/configs/nusc/pp/nusc_v10mini_pp.py'
    cfg = Config.fromfile(config_file)
    train_config = cfg.data.train
    dataset = build_dataset(cfg.data.train)
    # dataset0 = dataset[0]
    # dataset = build_dataset(cfg.data.val)
    # print(dataset.__len__())
    #
    # for i in range(100):
    #     data = dataset.__getitem__(i)
    #     break
    # print(11)

    data_loader = DataLoader(dataset,batch_size=1,shuffle=False,
            num_workers=2,collate_fn=collate_kitti,pin_memory=False,)

    frame = 0

    for i, data_batch in enumerate(data_loader):
        example = example_to_device(
            data_batch, 'cuda', non_blocking=False)

        if i == frame:
            image0 = example['img'][0][0].to(device="cpu").numpy()
            image0 = image0.swapaxes(0, 1)
            image0 = image0.swapaxes(1, 2)

            plt.imshow(image0)
            plt.show()
            image0[:, :, [0, 1, 2]] = image0[:, :, [2, 1, 0]]
            plt.imshow(image0)
            plt.show()

            # cv2.imshow('cam0',image0.numpy())
            # cv2.waitKey(0)

            # image0=example['img'][0][0].to(device="cpu")
            # image0 = image0.swapaxes(0, 1)
            # image0 = image0.swapaxes(1, 2)
            # plt.imshow(image0.numpy())
            # plt.show()
            #
            # image0 = example['img'][0][1].to(device="cpu")
            # image0 = image0.swapaxes(0, 1)
            # image0 = image0.swapaxes(1, 2)
            # plt.imshow(image0.numpy())
            # plt.show()
            #
            # image0 = example['img'][0][2].to(device="cpu")
            # image0 = image0.swapaxes(0, 1)
            # image0 = image0.swapaxes(1, 2)
            # plt.imshow(image0.numpy())
            # plt.show()
            #
            # image0 = example['img'][0][3].to(device="cpu")
            # image0 = image0.swapaxes(0, 1)
            # image0 = image0.swapaxes(1, 2)
            # plt.imshow(image0.numpy())
            # plt.show()
            #
            # image0 = example['img'][0][4].to(device="cpu")
            # image0 = image0.swapaxes(0, 1)
            # image0 = image0.swapaxes(1, 2)
            # plt.imshow(image0.numpy())
            # plt.show()
            #
            # image0 = example['img'][0][5].to(device="cpu")
            # image0 = image0.swapaxes(0, 1)
            # image0 = image0.swapaxes(1, 2)
            # plt.imshow(image0.numpy())
            # plt.show()
            break

        print("test-only")

    model_conf=cfg.model
    train_conf=cfg.train_cfg
    test_conf=cfg.test_cfg
    model = build_detector(cfg.model, train_cfg=cfg.train_cfg, test_cfg=cfg.test_cfg)
    model = model.cuda()
    # model.eval()

    for i, data_batch in enumerate(data_loader):
        example = example_to_device(
            data_batch, 'cuda', non_blocking=False
        )
        losses = model(example, return_loss=True)
        print('loss', losses)
        break


