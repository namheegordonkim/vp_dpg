from threading import Thread

import dearpygui.dearpygui as dpg
import hydra
from omegaconf import DictConfig
from vispy import scene, app


def visualize_dpg_controller():
    dpg.create_context()
    dpg.configure_app(manual_callback_management=True)
    with dpg.window(label="Hello World", modal=False, show=True, width=400, height=400, tag="window-controller"):
        dpg.add_text(label="", tag="value-epochs_so_far", default_value="Hello World")

    dpg.create_viewport(title='Vispy and DearPyGui', width=400, height=400)
    dpg.setup_dearpygui()
    dpg.show_viewport()

    # to enable debugger
    while dpg.is_dearpygui_running():
        jobs = dpg.get_callback_queue()
        dpg.run_callbacks(jobs)
        dpg.render_dearpygui_frame()

    dpg.destroy_context()


@hydra.main(config_name="config.yaml", config_path="./", version_base=None)
def main(cfg: DictConfig):
    if cfg["debug_yes"]:
        import pydevd_pycharm
        pydevd_pycharm.settrace('localhost', port=12345, stdoutToServer=True, stderrToServer=True, suspend=False)

    # simultaneous visualization of GUI and landscape
    canvas = scene.SceneCanvas(keys='interactive', bgcolor='white', size=(800, 600), show=True)
    # view = canvas.central_widget.add_view()
    view = scene.widgets.ViewBox(parent=canvas.scene, border_color='b', )
    view.camera = scene.TurntableCamera(up='z', azimuth=-30, fov=1.0, distance=800)
    view.camera.rect = 0, 0, 1, 1
    view.camera.center[0] += 10

    @canvas.events.resize.connect
    def resize(event=None):
        view.pos = 0, 0
        view.size = canvas.size

    resize()
    canvas.show()

    dpg_proc = Thread(target=visualize_dpg_controller, args=())
    dpg_proc.start()
    app.run()
    dpg_proc.join()


if __name__ == "__main__":
    main()
