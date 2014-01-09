from maya import OpenMayaRender #(1)
renderer = OpenMayaRender.MHardwareRenderer
glFT = renderer.theRenderer().glFunctionTable()

class Shape(object): #(2)
    def coords(self): #(3)
        """Return a list of groups of points,
        each group defining a line segment."""
        return []

    def draw(self, m3dview): #(4)
        m3dview.beginGL() #(5)
        for segmentcoords in self.coords(): #(6)
            glFT.glBegin(OpenMayaRender.MGL_LINE_STRIP) #(7)
            for coords in segmentcoords: #(8)
                glFT.glVertex3f(*coords)
            glFT.glEnd() #(9)
        m3dview.endGL() #(10)

class Cross(Shape): #(1)
    def coords(self): #(2)
        return [
           ((-10, 0, 0), (10, 0, 0)),
           ((0, -10, 0), (0, 10, 0)),
           ((0, 0, -10), (0, 0, 10)),]

class Square(Shape): #(3)
    def coords(self): #(4)
        return [
            ((20, 20, 0),
             (20, -20, 0),
             (-20, -20, 0),
             (-20, 20, 0),
             (20, 20, 0))]

class CrossInSquare(Cross, Square):
    def coords(self):
        result = Cross.coords(self)
        result.extend(Square.coords(self))
        return result


def testdraw():
    from maya import OpenMayaUI #(1)
    m3dview = OpenMayaUI.M3dView.active3dView() #(2)
    m3dview.beginOverlayDrawing() #(3)
    Square().draw(m3dview) #(4)
    Cross().draw(m3dview)
    #CrossInSquare().draw(m3dview)
    m3dview.endOverlayDrawing() #(5)
