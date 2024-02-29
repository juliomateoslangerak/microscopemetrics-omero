from hypothesis import given, settings
from microscopemetrics_schema import strategies as st_mm_sch

from omero.gateway import (
    CommentAnnotationWrapper,
    DatasetWrapper,
    FileAnnotationWrapper,
    ImageWrapper,
    MapAnnotationWrapper,
    ProjectWrapper,
    RoiWrapper,
    TagAnnotationWrapper,
)

import microscopemetrics_omero.dump as dump


# def test_dump_image_process(conn, mm_finished_analysis, project_structure):
#     image_info = project_structure["image_info"]
#     im_id = image_info["image_0.czi"]
#     image = conn.getObject("Image", im_id)
#     dump.dump_image_process(conn, image, mm_finished_analysis, "test_namespace")
#
#
def test_dump_image(conn, mm_image5d_fixture, project_structure):
    dataset_info = project_structure["dataset_info"]
    ds_id = dataset_info["dataset_0"]
    dataset = conn.getObject("Dataset", ds_id)

    image_obj = dump.dump_image(
        conn=conn, image=mm_image5d_fixture, target_dataset=dataset
    )
    assert image_obj is not None
    assert isinstance(image_obj, ImageWrapper)
    assert isinstance(image_obj.getId(), int)


@given(roi=st_mm_sch.st_mm_roi())
def test_dump_roi(conn, roi, project_structure):
    image_info = project_structure["image_info"]
    im_id = image_info["image_0.czi"]
    image = conn.getObject("Image", im_id)
    roi_obj = dump.dump_roi(conn=conn, roi=roi, target_image=image)

    assert roi_obj is not None
    assert isinstance(roi_obj, RoiWrapper)
    assert isinstance(roi_obj.getId(), int)


@given(tag=st_mm_sch.st_mm_tag())
def test_dump_tag(conn, tag, project_structure):
    image_info = project_structure["image_info"]
    im_id = image_info["image_0.czi"]
    image = conn.getObject("Image", im_id)
    dataset = image.getParent()
    project = dataset.getParent()

    # this is creating separate tags
    image_tag_obj = dump.dump_tag(conn=conn, tag=tag, target_object=image)
    dataset_tag_obj = dump.dump_tag(conn=conn, tag=tag, target_object=dataset)
    project_tag_obj = dump.dump_tag(conn=conn, tag=tag, target_object=project)

    assert image_tag_obj is not None
    assert isinstance(image_tag_obj, TagAnnotationWrapper)
    assert isinstance(image_tag_obj.getId(), int)
    assert dataset_tag_obj is not None
    assert isinstance(dataset_tag_obj, TagAnnotationWrapper)
    assert isinstance(dataset_tag_obj.getId(), int)
    assert project_tag_obj is not None
    assert isinstance(project_tag_obj, TagAnnotationWrapper)
    assert isinstance(project_tag_obj.getId(), int)


@given(key_values=st_mm_sch.st_mm_key_values())
def test_dump_key_value(conn, key_values, project_structure):
    image_info = project_structure["image_info"]
    im_id = image_info["image_0.czi"]
    image = conn.getObject("Image", im_id)
    dataset = image.getParent()
    project = dataset.getParent()

    image_kv_obj = dump.dump_key_value(
        conn=conn, key_values=key_values, target_object=image
    )
    dataset_kv_obj = dump.dump_key_value(
        conn=conn, key_values=key_values, target_object=dataset
    )
    project_kv_obj = dump.dump_key_value(
        conn=conn, key_values=key_values, target_object=project
    )

    assert image_kv_obj is not None
    assert isinstance(image_kv_obj, MapAnnotationWrapper)
    assert isinstance(image_kv_obj.getId(), int)
    assert dataset_kv_obj is not None
    assert isinstance(dataset_kv_obj, MapAnnotationWrapper)
    assert isinstance(dataset_kv_obj.getId(), int)
    assert project_kv_obj is not None
    assert isinstance(project_kv_obj, MapAnnotationWrapper)
    assert isinstance(project_kv_obj.getId(), int)


def test_dump_table_as_dict(conn, mm_table_as_dict_fixture, project_structure):
    image_info = project_structure["image_info"]
    im_id = image_info["image_0.czi"]
    image = conn.getObject("Image", im_id)
    dataset = image.getParent()
    project = dataset.getParent()

    image_table_obj = dump.dump_table(
        conn=conn, table=mm_table_as_dict_fixture, omero_object=image
    )
    dataset_table_obj = dump.dump_table(
        conn=conn, table=mm_table_as_dict_fixture, omero_object=dataset
    )
    project_table_obj = dump.dump_table(
        conn=conn, table=mm_table_as_dict_fixture, omero_object=project
    )

    assert image_table_obj is not None
    assert isinstance(image_table_obj, FileAnnotationWrapper)
    assert isinstance(image_table_obj.getId(), int)
    assert dataset_table_obj is not None
    assert isinstance(dataset_table_obj, FileAnnotationWrapper)
    assert isinstance(dataset_table_obj.getId(), int)
    assert project_table_obj is not None
    assert isinstance(project_table_obj, FileAnnotationWrapper)
    assert isinstance(project_table_obj.getId(), int)


def test_dump_table_as_pandas_df(
    conn, mm_table_as_pandas_df_fixture, project_structure
):
    image_info = project_structure["image_info"]
    im_id = image_info["image_0.czi"]
    image = conn.getObject("Image", im_id)
    dataset = image.getParent()
    project = dataset.getParent()

    image_table_obj = dump.dump_table(
        conn=conn, table=mm_table_as_pandas_df_fixture, omero_object=image
    )
    dataset_table_obj = dump.dump_table(
        conn=conn, table=mm_table_as_pandas_df_fixture, omero_object=dataset
    )
    project_table_obj = dump.dump_table(
        conn=conn, table=mm_table_as_pandas_df_fixture, omero_object=project
    )

    assert image_table_obj is not None
    assert isinstance(image_table_obj, FileAnnotationWrapper)
    assert isinstance(image_table_obj.getId(), int)
    assert dataset_table_obj is not None
    assert isinstance(dataset_table_obj, FileAnnotationWrapper)
    assert isinstance(dataset_table_obj.getId(), int)
    assert project_table_obj is not None
    assert isinstance(project_table_obj, FileAnnotationWrapper)
    assert isinstance(project_table_obj.getId(), int)


@given(comment=st_mm_sch.st_mm_comment())
@settings(max_examples=1)
def test_dump_comment(conn, comment, project_structure):
    image_info = project_structure["image_info"]
    im_id = image_info["image_0.czi"]
    image = conn.getObject("Image", im_id)
    dataset = image.getParent()
    project = dataset.getParent()

    image_comment_obj = dump.dump_comment(
        conn=conn, comment=comment, omero_object=image
    )
    dataset_comment_obj = dump.dump_comment(
        conn=conn, comment=comment, omero_object=dataset
    )
    project_comment_obj = dump.dump_comment(
        conn=conn, comment=comment, omero_object=project
    )

    assert image_comment_obj is not None
    assert isinstance(image_comment_obj, CommentAnnotationWrapper)
    assert isinstance(image_comment_obj.getId(), int)
    assert dataset_comment_obj is not None
    assert isinstance(dataset_comment_obj, CommentAnnotationWrapper)
    assert isinstance(dataset_comment_obj.getId(), int)
    assert project_comment_obj is not None
    assert isinstance(project_comment_obj, CommentAnnotationWrapper)
    assert isinstance(project_comment_obj.getId(), int)
