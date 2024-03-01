import csv
import glob
import os
import shutil

import numpy as np
import supervisely as sly
from cv2 import connectedComponents
from dataset_tools.convert import unpack_if_archive
from supervisely.io.fs import (
    file_exists,
    get_file_name,
    get_file_name_with_ext,
    get_file_size,
)
from tqdm import tqdm

import src.settings as s


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    # Possible structure for bbox case. Feel free to modify as you needs.

    dataset_path = "/home/alex/DATASETS/TODO/MP-IDB"
    images_folder = "img"
    anns_folder = "gt"
    bboxes_path = "/home/alex/DATASETS/TODO/MP-IDB/Falciparum/mp-idb-falciparum.csv"
    batch_size = 5
    ds_name = "ds"

    def fix_masks(image_np: np.ndarray) -> np.ndarray:
        lower_bound = np.array([70, 110, 0])
        upper_bound = np.array([255, 255, 255])
        condition_white = np.logical_and(
            np.all(image_np >= lower_bound, axis=2), np.all(image_np <= upper_bound, axis=2)
        )

        lower_bound = np.array([0, 0, 0])
        upper_bound = np.array([20, 20, 20])
        condition_black = np.logical_and(
            np.all(image_np >= lower_bound, axis=2), np.all(image_np <= upper_bound, axis=2)
        )

        image_np[np.where(condition_white)] = (255, 255, 255)
        image_np[np.where(condition_black)] = (0, 0, 0)

        return image_np

    def create_ann(image_path):
        labels = []
        tags = []

        # image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = 1944  # image_np.shape[0]
        img_wight = 2592  #  image_np.shape[1]

        obj_class_name = image_path.split("/")[-3]
        obj_class = meta.get_obj_class(obj_class_name.lower())

        im_name = get_file_name(image_path)
        tags_data = im_name.split("-")[-1].split("_")
        for tag_data in tags_data:
            curr_meta = letter_to_meta[tag_data]
            tag = sly.Tag(curr_meta)
            tags.append(tag)

        mask_path = image_path.replace("img", "gt")

        if file_exists(mask_path):
            # mask_np = sly.imaging.image.read(mask_path)[:, :, 0]
            mask_np = sly.imaging.image.read(mask_path)[:, :, :]
            mask_np = fix_masks(mask_np)[:, :, 0]
            mask = mask_np == 255
            ret, curr_mask = connectedComponents(mask.astype("uint8"), connectivity=8)
            for i in range(1, ret):
                obj_mask = curr_mask == i
                curr_bitmap = sly.Bitmap(obj_mask)
                curr_label = sly.Label(curr_bitmap, obj_class)
                labels.append(curr_label)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=tags)

    falciparum = sly.ObjClass("falciparum", sly.AnyGeometry)
    malariae = sly.ObjClass("malariae", sly.Bitmap)
    ovale = sly.ObjClass("ovale", sly.Bitmap)
    vivax = sly.ObjClass("vivax", sly.Bitmap)

    ring_stage_meta = sly.TagMeta("ring stage", sly.TagValueType.NONE)
    trophozoite_stage_meta = sly.TagMeta("trophozoite stage", sly.TagValueType.NONE)
    schizont_stage_meta = sly.TagMeta("schizont stage", sly.TagValueType.NONE)
    gametocyte_stage_meta = sly.TagMeta("gametocyte stage", sly.TagValueType.NONE)

    letter_to_meta = {
        "R": ring_stage_meta,
        "T": trophozoite_stage_meta,
        "S": schizont_stage_meta,
        "G": gametocyte_stage_meta,
    }

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(
        obj_classes=[falciparum, malariae, ovale, vivax],
        tag_metas=[
            ring_stage_meta,
            trophozoite_stage_meta,
            schizont_stage_meta,
            gametocyte_stage_meta,
        ],
    )
    api.project.update_meta(project.id, meta.to_json())

    dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

    images_pathes = glob.glob(dataset_path + "/*/img/*.jpg")

    progress = sly.Progress("Create dataset {}".format(ds_name), len(images_pathes))

    for img_pathes_batch in sly.batched(images_pathes, batch_size=batch_size):
        img_names_batch = [get_file_name_with_ext(im_path) for im_path in img_pathes_batch]

        img_infos = api.image.upload_paths(dataset.id, img_names_batch, img_pathes_batch)
        img_ids = [im_info.id for im_info in img_infos]

        anns = [create_ann(image_path) for image_path in img_pathes_batch]
        api.annotation.upload_anns(img_ids, anns)

        progress.iters_done_report(len(img_names_batch))

    return project
