from manim import *
from numpy import *

class Func:
    ig = 3E-4
    rg = 160.0
    r1 = 3375.0
    r2 = 3375.0
    rs = 5000.0
    rt75 = 746.0

    @staticmethod
    def getE():
        return (Func.ig * (
                Func.rg * (Func.r1 + Func.rt75) * (Func.r2 + Func.rs) +
                (Func.r1 * Func.r2 * Func.rs) +
                (Func.r1 * Func.r2 * Func.rt75) +
                (Func.r1 * Func.rs * Func.rt75) +
                (Func.r2 * Func.rs * Func.rt75)
        )
                ) / (Func.r1 * Func.rs - Func.r2 * Func.rt75)

    @staticmethod
    def f_i_r(rx):
        e = Func.getE()
        return (Func.r1 * Func.rs - Func.r2 * rx) * e / (
                Func.rg * (Func.r1 + rx) * (Func.r2 + Func.rs) +
                (Func.r1 * Func.r2 * Func.rs) +
                (Func.r1 * Func.r2 * rx) +
                (Func.r1 * Func.rs * rx) +
                (Func.r2 * Func.rs * rx)
        )

    @staticmethod
    def f_r_t(t):
        b = 3950.0
        t0 = 25.0
        r_t0 = 5000.0
        return r_t0 * math.e ** (b * (1.0 / (t + 273.15) - 1.0 / (t0 + 273.15)))

    @staticmethod
    def f_i_t(t):
        return 10E3 * Func.f_i_r(Func.f_r_t(t))

    @staticmethod
    def line(t):
        return Func.ig * 10E3 / (75 - 25) * t - 1.5

    @staticmethod
    def delta_t(t):
        return 3 * (Func.f_i_t(t) - Func.line(t))

    @staticmethod
    def setR12(value):
        Func.r1 = Func.r2 = value


class TransformScene(Scene):
    def construct(self):
        # 绘制函数
        # 坐标轴 轴线
        mAxes = Axes(
            x_range = [0,2,1],
            y_range = [0,2,1],
            x_length = 6,
            y_length = 6
        )
        # mAxesLabel = mAxes.get_axis_labels(x_label="T/°C", y_label="I/A")

        mTracker = ValueTracker(1)

        graph = mAxes.plot(
            lambda x:x**mTracker.get_value(),
            color=BLUE,
            x_range=[0, 5]
        )
        graph1 = mAxes.plot(
            lambda x:x**0.5,
            color=PURPLE,
            x_range=[0, 5]
        )
        mtrace = VGroup()
        for i in arange(0.1,1,0.05):
            subtrace = mAxes.plot(lambda x: x**i,x_range=[0,5])
            mtrace += subtrace
        for i in arange(1,5,0.1):
            subtrace = mAxes.plot(lambda x: x**i,x_range=[0,5])
            mtrace += subtrace
        mtp = mtrace[0]



        # point = Dot(radius=1).add_updater(
        #     lambda x : x.set_x(mTracker.get_value())
        # )
        self.add(graph)
        self.add(graph1)
        self.play(Create(mtp))
        for i in mtrace:
            self.play(
                Transform(mtp,
                          i,
                          rate_func = rate_functions.linear,
                          run_time=0.2
                          )
            )
            self.remove(mtp)
            mtp = i



class ApproScene(MovingCameraScene):
    def construct(self):

        Func.setR12(3105)

        mAxes = Axes(
            x_range=[20, 82, 10],
            x_axis_config=dict(include_tip=True),
            y_range=[0, 3.9, 1],
            y_axis_config=dict(include_tip=True, tick_size=0.1),
            x_length = 10,
            y_length = 7
        )

        mAxesLabel = mAxes.get_axis_labels(
            x_label=MathTex("I(mA)", font_size=30).next_to(mAxes.y_axis.get_corner(UR), RIGHT, SMALL_BUFF),
            y_label=MathTex("T(\\textdegree C)", font_size=50).next_to(mAxes.x_axis.get_corner(UR), UP, SMALL_BUFF)
        )

        subTrace = mAxes.plot(
            Func.f_i_t,
            x_range=[23, 75],
            color=YELLOW_A
        )
        gTarget = mAxes.plot(
            Func.line,
            x_range = [23,75],
            color = GRAY_B
        )

        # area = mAxes.get_area(
        #     subTrace, [25, 75],
        #     bounded_graph=gTarget,
        #     # color=,
        #     opacity=0.5
        # )

        mDot = Dot(
            mAxes.i2gp(gTarget.t_min, gTarget),
            color = GRAY_C,
            radius = 0.03
        )
        dotStart = Dot(
            mAxes.i2gp(gTarget.t_min, gTarget),
            color=GRAY,
            radius = 0.07
        )
        dotDesti = Dot(
            mAxes.i2gp(gTarget.t_max, gTarget),
            color=GRAY_C,
            radius=0.07
        )

        def update_curve(mob):
            mob.move_to(mDot.get_center())
        self.camera.frame.add_updater(update_curve)
        self.add(
            mAxes,
            mAxesLabel,
            # area,
            subTrace,
            gTarget,
            dotStart,
            dotDesti,
            mDot
        )
        self.play(
            self.camera.frame.animate.scale(0.1).move_to(mDot)
        )
        self.play(
            MoveAlongPath(
                mDot,
                gTarget,
                rate_func = linear,
                run_time = 5
            ))
        self.camera.frame.remove_updater(update_curve)
        self.wait(1)




# examples
from manim import *

class FollowingGraphCamera(MovingCameraScene):
    def construct(self):
        self.camera.frame.save_state()

        # create the axes and the curve
        ax = Axes(x_range=[-1, 10], y_range=[-1, 10])
        graph = ax.plot(lambda x: np.sin(x), color=BLUE, x_range=[0, 3 * PI])

        # create dots based on the graph
        moving_dot = Dot(ax.i2gp(graph.t_min, graph), color=ORANGE)
        dot_1 = Dot(ax.i2gp(graph.t_min, graph))
        dot_2 = Dot(ax.i2gp(graph.t_max, graph))

        self.add(ax, graph, dot_1, dot_2, moving_dot)
        self.play(self.camera.frame.animate.scale(0.5).move_to(moving_dot))

        def update_curve(mob):
            mob.move_to(moving_dot.get_center())

        self.camera.frame.add_updater(update_curve)
        self.play(MoveAlongPath(moving_dot, graph, rate_func=linear))
        self.camera.frame.remove_updater(update_curve)

        self.play(Restore(self.camera.frame))