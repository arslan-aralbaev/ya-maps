import pygame as pg


class Button:
    def __init__(self, screen: pg.Surface, x: int, y: int, sx: int, sy:int, color, grad=255, bor_grad=0.5, text="", font=20, text_color=[0, 0, 0]):
        self.plot, self.sc, self.llf, self.grad, self.an_flag = pg.Surface((sx, sy)), screen, False, grad, None
        self.x, self.y, self.sx, self.sy, self.col, self.an_plot = x, y, sx, sy, color[:], pg.Surface((sx, sy))
        self.font, self.text, self.text_c, self.bg = pg.font.SysFont(None, font), text, text_color, bor_grad
        self.an_cord, self.an_color, self.an_grad, self.an_time = (0, 0), [0, 0, 0], 0, pg.time.get_ticks()
        self.render(color)

    def render(self, color):
        """updating Button surface"""
        self.plot.fill([0, 0, 0])
        self.plot.set_alpha(self.grad)
        bor = int(min(self.sx, self.sy) / 2 * self.bg)
        pg.draw.rect(self.plot, color, (0, 0, self.sx, self.sy), border_radius=bor)
        pg.draw.rect(self.plot, list(map(lambda g: int(g * 0.6), color)), (0, 0, self.sx, self.sy), 2, border_radius=bor)
        text = self.font.render(self.text, True, self.text_c)
        self.plot.blit(text, text.get_rect(center=self.plot.get_rect().center))
        self.plot.set_colorkey([0, 0, 0])
        if self.an_flag is not None:
            self.an_plot.fill([0, 0, 0])
            self.an_plot.set_alpha(self.an_grad)
            pg.draw.circle(self.an_plot, self.an_color, self.an_cord, self.an_flag)
            self.plot.set_colorkey([0, 0, 0])
            if self.an_flag ** 2 > self.sx ** 2 + self.sy ** 2:
                x, y = pg.mouse.get_pos()
                lf = x in range(self.x, self.x + self.sx) and y in range(self.y, self.y + self.sy)
                self.an_flag, self.llf = None, not lf
            elif self.an_time + 3 < pg.time.get_ticks():
                self.an_time = pg.time.get_ticks()
                self.an_flag += 3
            self.plot.blit(self.an_plot, (0, 0), special_flags=pg.BLEND_RGB_SUB)

    def show(self, x, y):
        lf = x in range(self.x, self.x + self.sx) and y in range(self.y, self.y + self.sy)
        if lf and not self.llf:
            self.llf = True
            self.render(list(map(lambda g: int(g * 0.7), self.col)))
        elif self.llf and not lf:
            self.llf = False
            self.render(self.col)
        elif self.an_flag is not None:
            self.render(self.col)
        self.sc.blit(self.plot, (self.x, self.y))
        return lf

    def task_animation(self, x, y, color, grad=30):
        self.an_grad, self.an_cord, self.an_color, self.an_flag = grad, (x - self.x, y - self.y), color, 0


class Switch:
    """colors should be RGB, grad should be in range(0, 255)"""
    def __init__(self, sc: pg.Surface, x: int, y: int, sx: int, sy: int, col_bor, col_off, col_on, border=4, grad=255, state=False, tick_time=20):
        self.x, self.y, self.sx, self.sy, self.col_bor, self.moo = x, y, sx, sy, col_bor, False
        self.plot, self.col_off, self.col_on, self.state = pg.Surface((sx, sy)), col_off, col_on, state
        self.bor, self.sc, self.grad, self.tk_k = border, sc, grad, tick_time
        self.rad, self.last_tick = (sy - 4 * self.bor) // 2, pg.time.get_ticks()
        self.ma, self.mi = sx - 2 * self.bor - self.rad, 2 * self.bor + self.rad
        self.step, self.las = (sx - 4 * self.bor) // 10, self.ma if state else self.mi
        self.render()

    def render(self):
        """updating Switch surface"""
        po = self.sy // 2
        self.plot.fill([0, 0, 0])
        self.plot.set_alpha(self.grad)
        if self.moo and pg.time.get_ticks() - self.tk_k > self.last_tick:
            self.last_tick = pg.time.get_ticks()
            self.las += self.step // 2 if self.state else -self.step // 2
            if not self.state and self.las in range(self.mi - self.step, self.mi):
                self.moo, self.las = False, self.mi
            if self.state and self.las in range(self.ma, self.ma + self.step):
                self.moo, self.las = False, self.ma
        pg.draw.rect(self.plot, self.col_off, (0, 0, self.sx, self.sy), border_radius=po)
        pg.draw.rect(self.plot, self.col_on, (0, 0, self.las, self.sy), border_top_left_radius=po, border_bottom_left_radius=po)
        pg.draw.rect(self.plot, self.col_bor, (0, 0, self.sx, self.sy), self.bor, border_radius=po)
        pg.draw.circle(self.plot, self.col_bor, (self.las, self.sy // 2), self.rad)
        self.plot.set_colorkey([0, 0, 0])

    def switch(self):
        """switching switch state"""
        self.moo, self.state = True, False if self.state else True

    def set_state(self, state):
        """set switch state"""
        self.moo, self.state = self.state != state, state

    def show(self, x, y):
        if self.moo:
            self.render()
        """((x - self.las) ** 2 + (y - self.sy // 2) ** 2) <= self.rad ** 2"""
        lf = x in range(self.x, self.x + self.sx) and y in range(self.y, self.y + self.sy)
        self.sc.blit(self.plot, (self.x, self.y))
        return lf

    def get_real_state(self):
        """returns real switch state"""
        return self.state if not self.moo else not self.state

    def get_finally_state(self):
        """returns finally switch state"""
        return self.state


class ProgressBar:
    def __init__(self, sc, x, y, sx, sy, col_bor, col_off, col_on, border=4, grad=255):
        self.x, self.y, self.sx, self.sy, self.col_bor = x, y, sx, sy, col_bor
        self.plot, self.col_off, self.col_on = pg.Surface((sx, sy)), col_off, col_on
        self.bor, self.sc, self.grad = border, sc, grad
        self.ma, self.mi = sx - self.bor, 4 * self.bor
        self.step, self.las = (self.ma - self.mi) / 100, 0
        self.render()

    def render(self):
        po, now = self.sy // 10, int(self.mi + self.step * self.las)
        self.plot.fill([0, 0, 0])
        self.plot.set_alpha(self.grad)
        pg.draw.rect(self.plot, self.col_off, (0, 0, self.sx, self.sy), border_radius=po)
        pg.draw.rect(self.plot, self.col_on, (0, 0, now, self.sy), border_radius=po)
        pg.draw.rect(self.plot, self.col_bor, (0, 0, self.sx, self.sy), self.bor, border_radius=po)
        self.plot.set_colorkey([0, 0, 0])

    def show(self, x, y):
        lf = x in range(self.x, self.x + self.sx) and y in range(self.y, self.y + self.sy)
        self.sc.blit(self.plot, (self.x, self.y))
        return lf

    def set_prog(self, per):
        if per > 0 and per <= 100:
            self.las = per
            self.render()

    def add_prog(self, per):
        if per > 0 and self.las + per <= 100:
            self.las += per
            self.render()


class TextBoxFixedX:
    def __init__(self, screen: pg.Surface, x: int, y: int, sx: int, sy: int, color, grad=255, text="", font=22,
                 text_color=[30, 30, 30], split_text=True, align="l", changeable=True, delta=0.5):
        """aligns: l - left; r - right, c - center;"""
        self.plot, self.sc, self.llf, self.grad = pg.Surface((sx, sy)), screen, False, grad
        self.x, self.y, self.sx, self.sy, self.col, self.r_sy = x, y, sx, sy, color[:], sy
        self.font, self.text, self.text_c = font, text, text_color
        self.an_cord, self.an_time, self.an_state, self.text_plot = (0, 0), pg.time.get_ticks(), False, pg.Surface((sx, sy))
        self.text_flag, self.align, self.red_mode, self.lines_text = split_text, align, False, []
        self.op_flag, self.t_sy, self.changeable, self.delta, self.op_time = 0, sy, changeable, delta, pg.time.get_ticks()
        self.render_text()
        self.render(color)


    def split_text(self, text):
        lsmax = self.sx - self.font
        font = pg.font.SysFont("calibri", self.font)
        print(font.size("abc"))
        trf, lp, ste = lsmax // 2, 0, 0
        if lsmax < 8:
            print("too small")
        rez, line = [], ""
        for si in text:
            if si == " " and ste == 0:
                continue
            if si == " ":
                lp = ste
            if font.size(line)[0] >= lsmax:
                if ste - lp > trf or ste - lp == 0:
                    rez.append(line)
                    line, ste, lp = "", -1, 0
                else:
                    rez.append(line[:lp])
                    line += si
                    line, ste, lp = line[lp + 1:], len(line[lp + 1:]) - 1, 0
            else:
                line += si
            ste += 1
        if line:
            rez.append(line)
        return rez

    def add_text(self, font, text, sx, sy):
        line = font.render(text, True, self.text_c)
        if self.align == "l":
            self.text_plot.blit(line, line.get_rect(topleft=[sx, sy]))
        elif self.align == "r":
            self.text_plot.blit(line, line.get_rect(topright=[sx, sy]))
        else:
            self.text_plot.blit(line, line.get_rect(centerx=sx, y=sy))

    def render_text(self):
        font = pg.font.SysFont("calibri", self.font)
        text = self.split_text(self.text)
        ls1, ls2 = self.font, int(self.font * self.delta)
        self.lines_text, self.r_sy = text[:], ls1 + (ls1 + ls2) * len(text)
        self.text_plot = pg.Surface((self.sx, self.r_sy))
        ddx = self.font // 2 if self.align == "l" else self.sx - self.font // 2 if self.align == "r" else self.sx // 2
        self.text_plot.fill([0, 0, 0])
        self.text_plot.set_alpha(self.grad)
        for i in range(len(text)):
            self.add_text(font, text[i], ddx, ls1 // 2 + (ls1 + ls2) * i)
        self.text_plot.set_colorkey([0, 0, 0])

    def render(self, col):
        bor = int(min(self.sx, self.sy) * 0.1)
        if self.op_flag == 1 and self.op_time + 20 < pg.time.get_ticks():
            self.op_time = pg.time.get_ticks()
            self.t_sy += 4
            if self.t_sy >= self.r_sy:
                self.t_sy, self.op_flag = self.r_sy, 0
            self.plot = pg.Surface((self.sx, self.t_sy))
        elif self.op_flag == -1 and self.op_time + 10 < pg.time.get_ticks():
            self.op_time = pg.time.get_ticks()
            self.t_sy -= 4
            if self.t_sy <= self.sy:
                self.t_sy, self.op_flag = self.sy, 0
            self.plot = pg.Surface((self.sx, self.t_sy))
        self.plot.fill([0, 0, 0])
        self.plot.set_alpha(self.grad)
        pg.draw.rect(self.plot, col, (0, 0, self.sx, self.t_sy), border_radius=bor)
        self.plot.blit(self.text_plot, (0, 0))
        pg.draw.rect(self.plot, list(map(lambda g: int(g * 0.6), col)), (0, 0, self.sx, self.t_sy), 2, border_radius=bor)
        if self.red_mode and self.an_time + 300 < pg.time.get_ticks():
            self.an_state = not self.an_state
        if self.red_mode:
            pg.draw.rect(self.plot, self.text_c, (*self.an_cord, 4, self.font), border_radius=bor)
        self.plot.set_colorkey([0, 0, 0])

    def show(self, x, y):
        lf = x in range(self.x, self.x + self.sx) and y in range(self.y, self.y + self.t_sy)
        if lf and not self.llf:
            self.llf = True
            self.render(list(map(lambda g: int(g * 0.7), self.col)))
        elif self.llf and not lf:
            self.llf = False
            self.render(self.col)
        elif self.red_mode and self.an_time + 300 < pg.time.get_ticks():
            self.render(self.col)
        elif self.op_flag:
            self.render(self.col)
        self.sc.blit(self.plot, (self.x, self.y))
        return lf

    def set_text(self, text):
        self.text = text
        self.render_text()

    def add_text_2(self, text):
        if not self.red_mode:
            return False
        else:
            pass