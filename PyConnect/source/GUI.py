import numpy, wx

from wx.glcanvas import GLCanvas
from OpenGL.GLU import *
from OpenGL.GL import *

__metaclass__ = type

class MyGLCanvas(GLCanvas):
    def __init__(self,parent, *args):
        super(MyGLCanvas, self).__init__(parent, attribList=[wx.glcanvas.WX_GL_DOUBLEBUFFER])
        self.lastx = self.x = 30
        self.lasty = self.y = 30
        self.size = None
        #self.red = 1.0
        #self.green = 1.0
        #self.blue = 1.0
        self.parent = parent
        #self.disconnect = DisconnectDraw()
        #self.monotonic = False
        #self.NodeSize = 1
        self.MouseRotate = False
        #self.colour = glColor3f(1.0, 0.0, 0.0)
        #print str(self.colour), 'hello'
        wx.EVT_PAINT(self, self.OnPaint)
        wx.EVT_SIZE(self, self.OnSize)
        wx.EVT_MOTION(self, self.OnMouseMotion)
        wx.EVT_LEFT_DOWN(self, self.OnMouseDown)
        wx.EVT_LEFT_UP(self, self.OnMouseUp)
        #wx.EVT_BUTTON(self, )
        wx.EVT_WINDOW_DESTROY(self, self.OnDestroy)
        
        self.init = True

    #ef ColourCheck(self, allow):
    #   if allow:
    #       self.red = 1.0
    #   else:
    #       self.red = 0.0
    #-----------------------------------------------------------------------------------------------
    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        self.SetCurrent()
        if not self.init:
            self.InitGL()
            self.init = True
        self.OnDraw()

    #-----------------------------------------------------------------------------------------------        
    def OnSize(self, event):
        size = self.size = self.GetClientSize()
        if self.GetContext():
            self.SetCurrent()
            glViewport(0, 0, size.width, size.height)
        event.Skip()

       
    #-----------------------------------------------------------------------------------------------
    def OnMouseDown(self, evt):
        self.CaptureMouse()
        #print self.CaptureMouse()
        self.x, self.y = self.lastx, self.lasty = evt.GetPosition()
    #-----------------------------------------------------------------------------------------------
    def OnMouseUp(self, evt):
        self.ReleaseMouse()
    #-----------------------------------------------------------------------------------------------
    def OnMouseMotion(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            self.MouseRotate = True
            self.lastx, self.lasty = self.x, self.y
            self.x, self.y = evt.GetPosition()
            self.Refresh(False)
        else: self.MouseRotate = False
    #-----------------------------------------------------------------------------------------------
    def OnDestroy(self, event):
        print "Destroying Window"

#====================================================================
class AxesDraw(MyGLCanvas):
    def __init__(self, parent):
        super(AxesDraw, self).__init__(parent)
        self.disc = parent.disc

    #-----------------------------------------------------------------------------------------------
    def InitGL(self):
        '''
        Initialize GL
        '''
       

        # set viewing projection
        glMatrixMode(GL_PROJECTION)
        glFrustum(-0.5, 0.5, -0.5, 0.5, 0.0, 3.0)

        # position viewer
        glMatrixMode(GL_MODELVIEW)
        glTranslatef(0.0, 0.0, -2.0)

        # position object
        glRotatef(self.y, 1.0, 0.0, 0.0)
        glRotatef(self.x, 0.0, 1.0, 0.0)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glShadeModel(GL_SMOOTH)
        
        

#--------------------------------------------------------------------
    
    def OnDraw(self):
        glClearColor(1.0,1.0,1.0,0.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.WireCube()
        
        for l in self.disc.basin_index['Level']:
            print self.disc.basin_index['Level'][l]
            if l !=1:
                for b in self.disc.basin_index['Level'][l]['Basin']:
                    c = self.disc.basin_index['Level'][l]['Basin'][b]\
                        ['Children']
                    p = self.disc.basin_index['Level'][l]['Basin'][b]\
                        ['Parents']
                    self.Lines(l,b,c,p)
        
        
        if self.size is None:
            self.size = self.GetClientSize()
            
        if self.MouseRotate:
            self.Rotate()
        
        self.SwapBuffers()

    #def AscertainLength(self):
        


    def Rotate(self):
        
        w, h = self.size
        w = max(w, 1.0)
        h = max(h, 1.0)
        xScale = 180.0 / w
        yScale = 180.0 / h
        glRotatef((self.y - self.lasty) * yScale, 1.0, 0.0, 0.0);
        glRotatef((self.x - self.lastx) * xScale, 0.0, 1.0, 0.0);


    def Lines(self, l, b, c, p):
        '''

        '''
        #print l,b,c, p
        red = self.disc.basin_index['Level'][l]['Basin'][b]['R']
        green = self.disc.basin_index['Level'][l]['Basin'][b]['G']
        blue = self.disc.basin_index['Level'][l]['Basin'][b]['B']
        
        x1 = self.disc.basin_index['Level'][l - 1]['Basin'][p]['X']-0.5
        y1 = self.disc.basin_index['Level'][l - 1]['Basin'][p]['Y']-0.5
        z1 = self.disc.basin_index['Level'][l - 1]['Z']#-0.5

        x2 = self.disc.basin_index['Level'][l]['Basin'][b]['X']-0.5
        y2 = self.disc.basin_index['Level'][l]['Basin'][b]['Y']-0.5
        if not c:                                              
            z2 = self.disc.basin_index['Level'][l]['Basin'][b]['Z']-0.5
        else:
            z2 = self.disc.basin_index['Level'][l]['Z']-0.5
        #print x1,y1,z1,x2,y2,z2
        print 'lines',l,b,c, x1, x2, y1, y2,z1, z2
        #print self.disc.basin_index['Level'][l]
        glBegin(GL_LINES)
        glColor3f(red, green, blue)
        glVertex3f(x1, y1, z1)
        glVertex3f(x2, y2, z2)
        glEnd()

    def Line(self, x_one, y_one, z_one, x_two, y_two, z_two, R, G, B):
        #
        #print x_one, y_one, z_one

        glBegin(GL_LINES)
        glColor3f(R, G, B)
        glVertex3f(x_one, y_one, z_one)
        glVertex3f(x_two, y_two, z_two)
        glEnd()

    def WireCube(self):
            # clear color and depth buffers
        #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glBegin(GL_LINES)
        #print self.red
        glColor3f(0,0,0)
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(0.5,-0.5,-0.5)

        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(-0.5,0.5,-0.5)

        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(-0.5,-0.5,0.5)

        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5, 0.5)

        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(0.5, -0.5, 0.5)

        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(0.5, 0.5, -0.5)

        glVertex3f(0.5, -0.5, -0.5)
        glVertex3f(0.5, -0.5, 0.5)

        glVertex3f(0.5, -0.5, -0.5)
        glVertex3f(0.5, 0.5, -0.5)

        glVertex3f(-0.5, 0.5, -0.5)
        glVertex3f(-0.5, 0.5, 0.5)

        glVertex3f(-0.5, 0.5, -0.5)
        glVertex3f(0.5, 0.5, -0.5)

        glVertex3f(-0.5, -0.5, 0.5)
        glVertex3f(0.5, -0.5, 0.5)

        glVertex3f(-0.5, -0.5, 0.5)
        glVertex3f(-0.5, 0.5, 0.5)

        glEnd()
    




#====================================================================

   

class ToolPanel(wx.Panel):
    def __init__(self,parent,id=-1, *args, **kwargs):
        super(ToolPanel, self).__init__(parent, id = -1, *args, **kwargs)
        self.canvas = id
        self.parent = parent
        self.helloButton = wx.Button(self, label = 'HELLO')
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.helloButton, flag = wx.TOP, border = 5)
        
        #self.border = wx.BoxSizer()

        self.SetSizer(self.sizer)
        

#===================================================================================================

class MainWin(wx.Frame):
    def __init__(self, disc,parent = None, id = -1, title = 'Disconnect'):
        super(MainWin, self).__init__(parent, id, title, size = (400,200), style = wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
        #wx.Frame.__init__(self, parent, id, title, size = (400,200), style = wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
        self.disc = disc
        self.parent = parent
        self.canvas = AxesDraw(self)
        self.panel = ToolPanel(self, self.parent)


        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.panel, proportion=0, flag=wx.EXPAND|wx.ALL, border=5)
        self.sizer.Add(self.canvas, proportion = 1, flag=wx.EXPAND|wx.ALL, border=5)
        self.SetSizer(self.sizer)

        self.Show()