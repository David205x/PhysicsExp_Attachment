from manim import *
from numpy import *
from scipy import *
import scipy.signal as sg

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
    def delta_i_t(t):
        return 3 * (Func.f_i_t(t) - Func.line(t))

    @staticmethod
    def setR12(value):
        Func.r1 = Func.r2 = value

    @staticmethod
    def delta_i_3D(r1, r2):
        Func.r1, r1 = r1, Func.r1
        Func.r2, r2 = r2, Func.r2
        t = range(25, 75)
        delta_i = Func.delta_i_t(t)
        z = np.polyfit(t, delta_i, 7)
        p = np.poly1d(z)
        delta_i_t_fitted = z(t)
        Func.r1 = r1
        Func.r2 = r2
        return sg.argrelmax(delta_i_t_fitted)


class MyScene(Scene):
    def construct(self):

        mAxes = Axes(
            x_range = [20, 82, 10],
            x_axis_config = dict(include_tip = True),
            y_range = [0, 3.9, 1],
            y_axis_config = dict(include_tip = True, tick_size = 0.1),
            x_length = 16,
            y_length = 8
        )

        mAxesLabel = mAxes.get_axis_labels(
            x_label = MathTex("I(mA)",font_size=30).next_to(mAxes.y_axis.get_corner(UR), RIGHT, SMALL_BUFF),
            y_label = MathTex("T(\\textdegree C)", font_size=50).next_to(mAxes.x_axis.get_corner(UR), UP, SMALL_BUFF)
        )

        mAxesVGroup = VGroup(mAxes)
        mAxesVGroup.scale(0.75).to_corner(UP)

        text, number, omg = num_text = VGroup(
            MathTex("R_{12} = "),
            DecimalNumber(
                Func.r1,
                num_decimal_places = 1,
            ),
            MathTex("\\Omega")
        )
        num_text.arrange(RIGHT)
        num_text.shift(3 * LEFT + 2 * UP)

        gph = always_redraw(
            lambda: mAxes.plot(
                Func.f_i_t, x_range=[23, 75], color=YELLOW
            )
        )
        line = mAxes.plot(
            Func.line, x_range=[23, 75], color=RED
        )
        delta_gph = always_redraw(
            lambda: mAxes.plot(Func.delta_i_t, x_range=[23, 75], color=YELLOW)
        )
        number_line = NumberLine(
            x_range = [2000, 5500, 2000],
            length = 4,
        ).shift(3*LEFT + 3*UP)


        self.play(Create(mAxesVGroup))
        self.play(Create(num_text))
        self.play(Create(number_line))
        self.play(Create(gph))
        self.play(Create(line))
        self.play(Create(delta_gph))
        self.play(ChangeDecimalToValue(number, 5500), run_time=3)

        number.set_value(2000)

        while Func.r1 <5500:
            self.wait(0.01)
            number.set_value(number.get_value())
            Func.setR12(number.get_value()+50)

class ITScene(Scene):
    def construct(self):

        axes_linear = Axes(
            x_range = [0,1],
            y_range = [0,1],
            x_length = 4,
            y_length = 4
        ).move_to(4*LEFT + 1.25*UP)
        graph_linear = axes_linear.plot(
            lambda x: x,
            color = YELLOW,
            x_range = [0,1]
        ).move_to(4*LEFT + 1.25*UP)


        axes_rush_into = Axes(
            x_range = [0,1],
            y_range = [0,1],
            x_length = 2,
            y_length = 2
        ).move_to(2.5*RIGHT + 2.5*UP)
        graph_rush_into = axes_rush_into.plot(
            lambda x: 0.5*np.arctan(3*x-1.5)+0.5,
            color = YELLOW,
            x_range = [0,1]
        ).move_to(2.5*RIGHT + 2.5*UP)

        axes_neg_linear = Axes(
            x_range = [0,1],
            y_range = [0,1],
            x_length = 2,
            y_length = 2
        ).move_to(5*RIGHT + 2.5*UP)
        graph_neg_linear = axes_rush_into.plot(
            lambda x: -1*x+1,
            color = YELLOW,
            x_range = [0,1]
        ).move_to(5*RIGHT + 2.5*UP)

        axes_there = Axes(
            x_range = [0,1],
            y_range = [0,1],
            x_length = 2,
            y_length = 2
        ).move_to(2.5*RIGHT)
        graph_there = axes_there.plot(
            lambda x: -4*x*(x-1),
            color = YELLOW,
            x_range = [0,1]
        ).move_to(2.5*RIGHT)

        axes_chaos = Axes(
            x_range = [0,1],
            y_range = [0,1],
            x_length = 2,
            y_length = 2
        ).move_to(5*RIGHT)
        graph_chaos = axes_chaos.plot(
            lambda x: 0.75*x + 0.2*np.sin(15*(x-0.3)),
            color = YELLOW,
            x_range = [0,1]
        ).move_to(5*RIGHT)


        self.play(
            Create(axes_linear),
            Create(graph_linear),
            Create(axes_rush_into),
            Create(graph_rush_into),
            Create(axes_neg_linear),
            Create(graph_neg_linear),
            Create(axes_there),
            Create(graph_there),
            Create(axes_chaos),
            Create(graph_chaos)
        )
        self.wait(1)

class NTCT(Scene):
    def construct(self):
        def F_r_t(x):
            return np.e**(7/(x+3)) - 1

        mAxes = Axes(
            x_range = [-1,8,2],
            y_range = [-1,20,21],
            x_length = 9,
            y_length = 7
        )
        mAxesLabel = mAxes.get_axis_labels(
            x_label = "t/°C",
            y_label =  MathTex("R/\Omega")
        )
        mGraph = mAxes.plot(
            F_r_t,
            color = BLUE,
            x_range = [-2,7]
        )
        mTracker = ValueTracker(-2)
        mInitial = [mAxes.coords_to_point(
            mTracker.get_value(),
            F_r_t(mTracker.get_value())
        )]
        mDot = Dot(point = mInitial)
        mDot.add_updater(
            lambda x: x.move_to(mAxes.c2p(
                mTracker.get_value(),
                F_r_t(mTracker.get_value())
            ))
        )
        mFormula = MathTex(
            "R(t) = ",
            "R_n",
            "* e^{",
            "B",
            "(\\frac{1}{t+273.15}-\\frac{1}{",
            "t_0",
            "+273.15})}").move_to(RIGHT * 1 + UP * 1)
        mFramebox_1 = SurroundingRectangle(mFormula[1], buff=.1)
        mFramebox_2 = SurroundingRectangle(mFormula[3], buff=.1)
        mFramebox_3 = SurroundingRectangle(mFormula[5], buff=.1)

        # mLines = [
        #     Line(0.5*LEFT+1.3*UP, RIGHT + 2*UP),
        #     Line(0.7*RIGHT+0.8*UP, RIGHT + 0.5*DOWN),
        #     Line(3*RIGHT+0.5*UP, 3.5*RIGHT)
        # ]
        mLines = [
            Line(np.array((-0.6,1.3,0)), np.array((-0.6,1.7,0))),
            Line(np.array((0.65,0.75,0)),  np.array((0.65,-0.2,0))),
            Line(np.array((2.95,0.7,0)),    np.array((2.95,0.3,0)))
        ]
        # mNotes = [
        #     Text("t_0下的热敏电阻阻值",font_size=30).move_to(3*RIGHT + 2*UP),
        #     Text("热敏电阻温度系数",font_size=30).move_to(2.7*RIGHT + 0.5*DOWN),
        #     Text("室温",font_size=30).move_to(4*RIGHT),
        # ]
        mNotes = [
            MathTex("t_0",font_size=30,color=GRAY).move_to(1.8*LEFT + 2*UP),
            Text("下的热敏电阻阻值",font_size=30, color=GRAY).move_to(2*UP),
            Text("热敏电阻温度系数",font_size=30, color=GRAY).move_to(0.5*RIGHT + 0.5*DOWN),
            Text("室温",font_size=30, color=GRAY).move_to(3*RIGHT),
        ]

        # 生成指定范围内指定个数的一维数组, 起始-终止的迭代器, 生成个数
        # mXSpace = np.linspace([-2,7],200)


        self.play(Create(mAxes))
        self.add(mAxesLabel,mDot)
        self.play(
            Write(mFormula),
            Create(mGraph),
            mTracker.animate.set_value(7),
            Write(mNotes[0]),
            Write(mNotes[1]),
            Write(mNotes[2]),
            Write(mNotes[3])
        )
        self.play(
            Create(mFramebox_1),
            Create(mFramebox_2),
            Create(mFramebox_3),
            Create(mLines[0]),
            Create(mLines[1]),
            Create(mLines[2])
        )
        self.wait(1)

class FinalScene(Scene):
    idx = 30
    def construct(self):
        # 坐标轴
        mAxes = Axes(
            x_range=[20, 82, 10],
            x_axis_config=dict(include_tip=True),
            y_range=[-1, 3.9, 1],
            y_axis_config=dict(include_tip=True, tick_size=0.1),
            x_length = 7,
            y_length = 7
        ).move_to(3*LEFT)
        # 坐标轴标记
        mAxesLabel = mAxes.get_axis_labels(
            x_label=MathTex("I(mA)", font_size=30),
            y_label=MathTex("T(\\textdegree C)", font_size=50)
        )

        mRefAxes = Axes(
            x_range=[600,5100,1000],
            y_range=[-1,1,0.5],
            x_length=5,
            y_length=2.9,
            tips=False
        ).move_to(3.5*RIGHT + 2.1*DOWN)
        mRefLabel = mRefAxes.get_axis_labels(
            x_label=MathTex("R_{1\&2}",font_size=30),
            y_label=MathTex("\\mid \\Delta T \\mid",font_size=30)
        )

        # I(F(t))映射函数
        gTarget = mAxes.plot(
            Func.line,
            x_range = [23,75],
            color = BLUE
        )
        Func.setR12(1920)
        gSouDelta = mAxes.plot(
            lambda x: Func.delta_i_t(x) / 3,
            x_range = [23,75],
            color = RED
        )

        # R_1&2 参数阻值可调范围
        mSlider = NumberLine(
            x_range = [600,5100,1000],
            length = 5
        ).move_to(2*UR + 1.5*RIGHT)
        mTracker = ValueTracker(1920)
        mPointer = Vector(0.5*DOWN).add_updater(
            lambda m: m.next_to(
                mSlider.n2p(mTracker.get_value()), UP
            ))
        mDashLine = VGroup(
            DashedLine(
                mSlider.n2p(mTracker.get_value()),
                mRefAxes.coords_to_point(10000, -1),
                color=GREEN
            ).move_to(
                mSlider.n2p(mTracker.get_value())
            ).add_updater(
                lambda m: m.move_to(mSlider.n2p(mTracker.get_value()))),
         DashedLine(
            mSlider.n2p(mTracker.get_value()),
            mRefAxes.coords_to_point(5000,-1),
            color=YELLOW
        ).move_to(
            mSlider.n2p(mTracker.get_value())
        ).add_updater(
            lambda m: m.move_to( mSlider.n2p(mTracker.get_value()))),
            DashedLine(
                mSlider.n2p(mTracker.get_value()),
                mRefAxes.coords_to_point(1920, -1),
                color=RED
            ).move_to(
                mSlider.n2p(mTracker.get_value())
            ).add_updater(
                lambda m: m.move_to(mSlider.n2p(mTracker.get_value())))

        )


        mRLabel_2 = MathTex("\Omega").add_updater(
            lambda m: m.next_to(mPointer,LEFT)
        )
        mRValue = DecimalNumber(FinalScene.idx,0).move_to(3*UL).add_updater(
            lambda m: m.next_to(mRLabel_2,LEFT)
        ).move_to(mRLabel_2,LEFT)
        mRLabel = MathTex("R_{1\&2} = ").move_to(3*UL).add_updater(
            lambda m: m.next_to(mRValue,LEFT)
        )


        def getPeakDot():
            minimum_x = optimize.fminbound(Func.delta_i_t, 25, 75)
            minimum = Func.delta_i_t(minimum_x)
            maximum_x = optimize.fminbound(lambda x: -Func.delta_i_t(x), 25, 75)
            maximum = Func.delta_i_t(maximum_x)

            minDot = Dot()
            maxDot = Dot()

            if abs(minimum) > abs(maximum):
                return VGroup(
                    minDot.set_points([mAxes.coords_to_point(maximum_x, maximum)]),
                    maxDot.set_points([mAxes.coords_to_point(minimum_x, minimum)]),
                    DashedLine(minDot.get_center(),mRefAxes.coords_to_point(3000,maximum),color=BLUE),
                    DashedLine(maxDot.get_center(), mRefAxes.coords_to_point(3000, minimum), color=RED),
                )
            else:
                return VGroup(
                    Dot(point = [mAxes.coords_to_point(minimum_x, minimum)]),
                    Dot(point=[mAxes.coords_to_point(maximum_x, maximum)]),
                    DashedLine(minDot.get_center(),mRefAxes.coords_to_point(3000,minimum),color=BLUE),
                    DashedLine(maxDot.get_center(),mRefAxes.coords_to_point(3000,maximum),color=RED)
                )

        #轨迹集计算
        mFitTrace = VGroup()
        mOffsetTrace = VGroup()
        mPeakTrace = VGroup()
        for i in arange(600,5000,44):
            Func.setR12(i)

            subTrace = mAxes.plot(
                Func.f_i_t,
                x_range = [23,75],
                color = YELLOW
            )
            mFitTrace += subTrace

            subTrace = mAxes.plot(
                Func.delta_i_t,
                x_range = [23,75],
                color = RED
            )
            mOffsetTrace += subTrace
            mPeakTrace += getPeakDot()


        # 随机的初始参数下标
        FinalScene.idx = 30
        def DrawTransition(start_idx, end_idx, speed, isRemain = False):
            step = 1
            if start_idx > end_idx:
                step = -1
            for i in range(start_idx, end_idx, step):
                value = 44 * i + 600
                self.play(
                    Transform(
                        mFitTrace[FinalScene.idx],
                        mFitTrace[i],
                        rate_func = rate_functions.linear,
                        run_time = speed
                    ),
                    Transform(
                        mOffsetTrace[FinalScene.idx],
                        mOffsetTrace[i],
                        rate_func=rate_functions.linear,
                        run_time=speed
                    ),
                    Transform(
                        mPeakTrace[FinalScene.idx],
                        mPeakTrace[i],
                        rate_func=rate_functions.linear,
                        run_time=speed
                    ),
                    ChangeDecimalToValue(mRValue,value,alpha=0.1),
                    mTracker.animate.set_value(value)
                )
                if (step == 1 and i != end_idx-1) or (step == -1 and i != end_idx+1):
                    self.remove(mFitTrace[FinalScene.idx])
                    self.remove(mOffsetTrace[FinalScene.idx])
                    self.remove(mPeakTrace[FinalScene.idx])
                FinalScene.idx = i

        self.play(
            mTracker.animate.set_value(1920),
            ChangeDecimalToValue(mRValue,1920)
        )
        self.play(
            Create(mAxes),
            Create(mSlider),
            Write(mAxesLabel),

            Create(gTarget),
            Create(mFitTrace[FinalScene.idx]),
            Create(gSouDelta),

            Create(mPointer),
            Create(mDashLine),
            Write(mRLabel),
            Write(mRLabel_2)
        )
        self.wait(3),
        self.play(
            Transform(
                gSouDelta,
                mOffsetTrace[FinalScene.idx]
            )
        )
        self.wait(1)
        self.remove(gSouDelta)

        DrawTransition(30,20,1)
        self.wait(1)
        self.play(
            Create(mRefAxes),
            Create(mRefLabel)
        )
        # DrawTransition(0,100,1)
        # self.wait(0.5)
        # DrawTransition(99,62,1)
        # self.play(
        #     ChangeDecimalToValue(mRValue, 3375),
        #     mTracker.animate.set_value(3375)
        # )
        self.wait(1)

class RIMappingScene(Scene):
    def construct(self):
        def f_r_t(x):
            return np.e**(7/(x+3)) - 1

        mRTAxes = Axes(
            x_range=[0, 8, 2],
            y_range=[-1, 5, 11],
            x_length=3,
            y_length=3
        ).move_to(5 * LEFT)
        mRTLabel = mRTAxes.get_axis_labels(
            x_label="t",
            y_label=MathTex("R")
        )


        mITAxes = Axes(
            x_range=[0, 80, 20],
            y_range=[-1, 5, 6],
            x_length=3,
            y_length=3,
        ).move_to(5 * RIGHT)
        mITLabel = mITAxes.get_axis_labels(
            x_label="t",
            y_label=MathTex("I")
        )

        gRT = mRTAxes.plot(
            f_r_t,
            x_range=[2.0, 7.5],
            color=YELLOW_A
        )
        gIT = mITAxes.plot(
            Func.line,
            x_range=[20, 75],
            color=YELLOW_A
        )

        pGroupRT = VGroup()
        pGroupIT = VGroup()
        pGroupPath = VGroup()
        colors = [RED,ORANGE,GOLD,YELLOW,WHITE,GREEN,TEAL,BLUE,"#506DE3",PURPLE]
        for i in range(0, 10, 1):
            dot = Dot(
                point = [mRTAxes.coords_to_point(0.5*i+2.5, f_r_t(0.5*i+2.5))],
                radius = 0.05,
                color = colors[i]
            )
            pGroupRT.add(dot)
            pGroupIT.add(
                Dot(
                    point = [mITAxes.coords_to_point(5*i+25, Func.line(5*i+25))],
                    radius = 0.05,
                    color = colors[i]
                )
            )
            pGroupPath.add(TracedPath(
                dot.get_center,
                dissipating_time=0.65,
                stroke_color = colors[i],
                stroke_opacity=[0, 1]
            ))


        self.add(mRTAxes, mITAxes, gRT, pGroupPath)
        self.play(
            Create(pGroupRT),
            Write(mRTLabel),
            Write(mITLabel)
        )
        self.wait(1)
        self.play(
            Transform(pGroupRT,
                      pGroupIT,
                      run_time = 2.0
                      )
        )
        self.play(
            Create(gIT)
        )
        self.wait(1)

class TIMappingScene(Scene):
    def construct(self):

        mAxes = Axes(
            x_range = [0,11,2],
            y_range = [0,5.5,1],
            x_length = 8,
            y_length = 6
        )
        mAxesLabel = mAxes.get_axis_labels(
            x_label = "t",
            y_label = "I"
        )

        mTracker = ValueTracker(0)
        mDot = Dot(
            radius = 0.1,
            color = YELLOW
        ).add_updater(
            lambda m: m.move_to(mAxes.c2p(mTracker.get_value(),mTracker.get_value()/2))
        )
        mDotX = Dot(
            radius = 0.1,
            color = YELLOW_B
        ).add_updater(
            lambda m: m.move_to(mAxes.c2p(mTracker.get_value(), 0))
        )
        mDotY = Dot(
            radius = 0.1,
            color = YELLOW_B
        ).add_updater(
            lambda m: m.move_to(mAxes.c2p(0, mTracker.get_value()/2))
        )

        def getLineX():
            mLineX = DashedLine(
                mDotX,
                mDot,
                dash_length = 0.6,
                dashed_ratio = 0.8,
                color="#71A0AB"
            )
            return mLineX
        def getLineY():
            mLineY = DashedLine(
                mDotY,
                mDot,
                dash_length = 0.6,
                dashed_ratio = 0.8,
                color = "#71A0AB"
            )
            return mLineY
        mLineX = always_redraw(getLineX)
        mLineY = always_redraw(getLineY)

        mTrace = TracedPath(
            mDot.get_center,
            1.2,
            LIGHT_GRAY
        )

        self.add(mTrace)
        self.play(
            Create(mAxes),
            Create(mAxesLabel),
            Create(mLineX),
            Create(mLineY),
            Create(mDotX),
            Create(mDotY),
            Create(mDot),
        )


        for i in range(2,12,2):
            tempDot = Dot(color = YELLOW_A).move_to(mDot)
            self.play(
                mTracker.animate.set_value(i),
                Create(tempDot)
            )

        self.wait(1)



