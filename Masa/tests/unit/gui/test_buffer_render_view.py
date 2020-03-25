import pytest

from Masa.gui import BufferRenderView


@pytest.fixture(name="buff", scope="function")
def buffer(m_buffer, ocv_video, data_handler):
    return m_buffer(ocv_video(length=100), target_width=640)


class Dims:
    """Class to produce some combination of width and height."""
    @staticmethod
    def values():
        dims = [
            # width x height
            (640, 540),
            (1080, 720),
            (640, 720),
        ]
        return dims
    @staticmethod
    def ids():
        return [f"W:{width}, H:{height}" for width, height in Dims.values()]


@pytest.fixture(name="brv", scope="function")
def buffer_render_view(request, qtbot):
    # width, height = request.param
    width, height = 640, 540
    # print("fixture:", width, height)
    brv = BufferRenderView(width=width, height=height)
    # print(brv.size())
    qtbot.add_widget(brv)
    # request.instance.brv = brv
    return brv


@pytest.mark.skip(reason="The dimension do not be as thought")
def test_dims(brv):
    pass


def test_receive_data(brv, m_buffer, data_handler):
    # from here
    data_handler.curr_frame.connect(brv.set_frame_r)
    data_handler.curr_data.connect(brv.set_data_r)

    # brv.add...
