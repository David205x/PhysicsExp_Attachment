from manim import *
from scipy import optimize
import math
import manim
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
    def setR1R2(r1,r2):
        Func.r1 = r1
        Func.r2 = r2

    @staticmethod
    def three_d_delta_t(t,r):
        Func.setR12(r)
        return Func.delta_i_t(t)
        # return np.array([t,r,np.sin(t*r)])
        # return np.array([t,r,3*(t-50)+2*(r-2000)])

    @staticmethod
    def three_d_delta_r(t):
        return Func.delta_i_t(t)

    @staticmethod
    def three_d_dr(r1,r2):
        Func.setR1R2(r1, r2)
        minimum_x = optimize.fminbound(Func.three_d_delta_r, 25, 75)
        minimum = Func.three_d_delta_r(minimum_x)
        maximum_x = optimize.fminbound(lambda x: -Func.three_d_delta_r(x), 25, 75)
        maximum = Func.three_d_delta_r(maximum_x)
        if (abs(maximum) > abs(minimum)):
            if abs(maximum)<20:
                return maximum
            else: return 20
        else:
            if abs(minimum)<20:
                return minimum
            else: return -20

    def three_d_test(t,r):
        # Func.setR12(r)
        # return np.array([t,r,Func.delta_t(t)])
        # return np.array([t,r,np.sin(t*r)])
        return np.array([t,r,0])

    @staticmethod
    def delta_i_3D(r1, r2):
        Func.r1, r1 = r1, Func.r1
        Func.r2, r2 = r2, Func.r2
        t_range = np.arange(25, 75, 0.1)
        detla_i_list = np.array([])
        for t in t_range:
            detla_i_list = np.append(detla_i_list, Func.delta_i_t(t))
        # z = np.polyfit(t_range, detla_i_list, 7)
        # p = np.poly1d(z)
        # delta_i_t_fitted = p(t)
        temp = Func.delta_i_t(optimize.fminbound(lambda x: -1 * Func.delta_i_t(x),25,75))
        Func.r1 = r1
        Func.r2 = r2
        print(temp)
        return np.array([r1, r2, temp])


class ThreeDTest(ThreeDScene):
    def construct(self):

        axes = ThreeDAxes(
            x_range=[15,85,10],
            y_range=[500,5500,1000],
            z_range=[-1,2,5],
            # x_length=5,
            # y_length=5,
            # z_length=5
        )
        x_text = axes.get_x_axis_label(Tex("$x$",color=RED))
        y_text = axes.get_y_axis_label(Tex("$y$",color=YELLOW))
        z_text = axes.get_z_axis_label(Tex("$z$",color=BLUE))
        # plane = Surface(
        #     lambda u,v: axes.c2p(u,v,Func.three_d_delta_t(u,v)),
        #     u_range=[25,75],
        #     v_range=[550,5000],
        #     resolution=32,
        #     fill_opacity=0.6
        # )
        plane = Surface(
            lambda u,v: axes.c2p(u,v,Func.delta_i_3D(u,v)),
            u_range=[25,75],
            v_range=[550,5000],
            resolution=32,
            fill_opacity=0.6
        )
        plane.set_fill_by_value(
            axes=axes,
            colorscale=[
                (RED, -1),
                (GOLD_C,-0.75),
                (YELLOW,-0.5),
                (GREEN_C, -0.25),
                (BLUE_D, -0),
                (GREEN_C, 0.25),
                (YELLOW,0.5),
                (GOLD_C, 0.75),
                (RED, 1)],
            axis=2)
        self.set_camera_orientation(
            #phi 和z+轴的夹角
            #theta 以x+为0度绕z轴转，y+为90
            phi=80 * DEGREES,
            theta=0 * DEGREES,
            zoom=0.8,
            focal_distance=10
            # frame_center=np.array([0,0,0])
        )
        self.add(axes,plane,x_text,y_text,z_text)
        self.begin_ambient_camera_rotation(rate=1)
        for i in range(90,110,10):
            self.wait(7)
            self.move_camera(phi=i * DEGREES)
        self.wait(7)
        self.stop_ambient_camera_rotation()

        # self.wait(1)
        # self.move_camera(theta=90 * DEGREES)
        # self.wait(1)
        # self.move_camera(focal_distance=10)
        # self.wait(1)
        # self.move_camera(gamma=10)
        # self.wait(1)
        # self.move_camera(frame_center=np.array([2,2,2]))
        # self.wait(1)

class ThreeDR(ThreeDScene):
    def construct(self):

        axes = ThreeDAxes(
            x_range=[500,5100,1000],
            y_range=[500,5100,1000],
            z_range=[-10,10,5]

        )
        x_text = axes.get_x_axis_label(Tex("$x$",color=RED))
        y_text = axes.get_y_axis_label(Tex("$y$",color=YELLOW))
        z_text = axes.get_z_axis_label(Tex("$z$",color=BLUE))

        plane = Surface(
            lambda u,v: axes.c2p(u,v,Func.three_d_dr(u,v)),
            u_range=[750, 5000],
            v_range=[750, 5000],
            resolution=36,
            fill_opacity=0.6
        )
        plane.set_fill_by_value(
            axes=axes,
            colorscale=[
                (PURPLE,-20),
                (RED, -10),
                (GOLD_C, -1.5),
                (YELLOW, -1),
                (GREEN_C, -0.5),
                (BLUE_D, 0),
                (GREEN_C, 0.5),
                (YELLOW, 1),
                (GOLD_C, 1.5),
                (RED, 2)],
            axis=2)

        self.set_camera_orientation(
            #phi 和z+轴的夹角
            #theta 以x+为0度绕z轴转，y+为90
            phi=75 * DEGREES,
            theta=0 * DEGREES,
            zoom=0.6,
            focal_distance=50
        )
        self.add(axes, plane, x_text, y_text, z_text)
        self.begin_ambient_camera_rotation(rate=1)
        self.wait(7)
        self.stop_ambient_camera_rotation()
        for i in range(0,100,10):
            self.set_camera_orientation(
                phi = i* DEGREES
            )
            self.wait(1)




class ParaSurface(ThreeDScene):
    def func(self, u, v):
        return np.array([np.cos(u) * np.cos(v), np.cos(u) * np.sin(v), u])

    def construct(self):
        axes = ThreeDAxes(x_range=[-4,4], x_length=8)
        # surface = Surface(
        #     lambda u, v: axes.c2p(*self.func(u, v)),
        #     u_range=[-PI, PI],
        #     v_range=[0, TAU],
        #     resolution=8,
        # )
        self.set_camera_orientation(theta=70 * DEGREES, phi=75 * DEGREES)
        self.add(axes)