"""

The module requires the package matplotlib https://matplotlib.org/
which can be installed via PIP.
"""

from typing import Optional, Tuple
import matplotlib.pyplot as plt

def pause(interval : int) -> None:
  """
  Run the GUI event loop for *interval* seconds.

  If there is an active visualiser window, it will be updated and displayed before the pause, and the GUI event loop (if any) will run during the pause.

  If there is no active visualiser window, sleep for *interval* seconds instead.
  """
  plt.pause(interval)

class _BlitManager:
    def __init__(self, canvas, animated_artists=()):
        """
        Parameters
        ----------
        canvas : FigureCanvasAgg
            The canvas to work with, this only works for sub-classes of the Agg
            canvas which have the `~FigureCanvasAgg.copy_from_bbox` and
            `~FigureCanvasAgg.restore_region` methods.

        animated_artists : Iterable[Artist]
            List of the artists to manage
        """
        self.canvas = canvas
        self._bg = None
        self._artists = []

        for a in animated_artists:
            self.add_artist(a)
        # grab the background on every draw
        self.cid = canvas.mpl_connect("draw_event", self.on_draw)

    def on_draw(self, event):
        """Callback to register with 'draw_event'."""
        cv = self.canvas
        if event is not None:
            if event.canvas != cv:
                raise RuntimeError
        self._bg = cv.copy_from_bbox(cv.figure.bbox)
        self._draw_animated()

    def add_artist(self, art):
        """
        Add an artist to be managed.

        Parameters
        ----------
        art : Artist

            The artist to be added.  Will be set to 'animated' (just
            to be safe).  *art* must be in the figure associated with
            the canvas this class is managing.

        """
        if art.figure != self.canvas.figure:
            raise RuntimeError
        art.set_animated(True)
        self._artists.append(art)

    def _draw_animated(self):
        """Draw all of the animated artists."""
        fig = self.canvas.figure
        for a in self._artists:
            fig.draw_artist(a)

    def update(self):
        """Update the screen with animated artists."""
        cv = self.canvas
        fig = cv.figure
        # paranoia in case we missed the draw event,
        if self._bg is None:
            self.on_draw(None)
        else:
            # restore the background
            cv.restore_region(self._bg)
            # draw all of the animated artists
            self._draw_animated()
            # update the GUI state
            cv.blit(fig.bbox)
        # let the GUI event loop process anything it has to do
        cv.flush_events()

def size(data) -> Tuple[int,int]:
  """
  Returns the height and width of the given 2D data.
  """
  try:
    height = len(data)
    width = len(data[0])
    if any( len(row) != width for row in data):      
      raise ValueError('Not 2D scalar data.')
  except (IndexError,TypeError):
    try:
      (height,width) = data.shape
    except (AttributeError,ValueError):
      raise ValueError('Not 2D scalar data.')
  if width > 0 and height > 0:
    return (height,width)
  else:
    raise ValueError('Not 2D scalar data.')

class BaseVisualiser:
  """
  Display 2D scalar data as a pseudocolors image on a 2D grid.
  """

  def __init__(self, data,
               grid_lines = True,
               ticks = True,
               cmap = 'viridis',
               vmin : Optional[float] = None,
               vmax : Optional[float] = None,
               title : Optional[str]=None, 
               window_title : Optional[str] = None):
    (height,width) = size(data)
    self._size = (height,width)
    fig, ax = plt.subplots()
    # titles
    if title:
      ax.set_title(title)
    if not window_title:
      window_title = 'Visualiser'
    fig.canvas.manager.set_window_title(window_title)    
    # listed to close events
    self._is_open = True
    def on_close(event):
      self._is_open = False
    fig.canvas.mpl_connect('close_event', on_close )
    # add data raster
    self._im = ax.imshow(data, cmap=cmap, vmin=vmin,vmax=vmax, animated=True)
    # add grid lines
    hlns = [ ax.axhline(-.5,color='black',linestyle='-', linewidth=1)]
    vlns = [ ax.axvline(-.5,color='black',linestyle='-', linewidth=1)]
    if grid_lines:
      hlns.extend( ax.axhline(y-.5,color='gray',linestyle='-', linewidth=1) 
                   for y in range(1,height,1) )
      vlns.extend( ax.axvline(x-.5,color='gray',linestyle='-', linewidth=1) 
                   for x in range(1,width,1) )
    if ticks:
      # remove middle ticks, if any
      #ax.set_xticks([ t for t in  ax.get_xticks() if t.is_integer() ])
      #ax.set_yticks([ t for t in  ax.get_yticks() if t.is_integer() ])
      ax.tick_params(top = True, labeltop = True, right = True, labelright = True)
    else:
      ax.tick_params(bottom = False, labelbottom = False, left = False, labelleft = False)
    # blitter
    self._bm = _BlitManager(fig.canvas, [self._im] + hlns + vlns)  
    # make sure our window is on the screen and drawn
    plt.show(block=False)
    plt.pause(.1)

  def size(self) -> Tuple[int,int]:
    """The height and width of the data that the visualiser can display."""
    return self._size

  def width(self) -> int:
    return self._size[1]

  def height(self) -> int:
    return self._size[0]

  def is_open(self) -> bool:
    """
    Whether the window managed by the visualiser is open or not.
    """
    return self._is_open

  def wait_close(self):
    """
    Suspends the current execution until the visualiser window is manually closed by the user.
    """
    plt.show()

  def set_data(self, data) -> None:
    """
    Sets the data displayed.
    """
    if self.is_open() :
      self._im.set_data(data)
      self._bm.update()

  def update(self, data, interval : int = 0.1) -> None:
    """ Sets the data displayed and pauses to the GUI event loop for *interval* seconds."""
    self.set_data(data)
    pause(interval)

class BinaryVisualiser(BaseVisualiser):  
  """
  Display 2D binary data as a black (1) and white (0) image on a 2D grid.
  """
  def __init__(self, data, title: Optional[str] = None, window_title: Optional[str] = None, grid_lines = True, ticks = True):
      super().__init__(data, cmap='binary',vmin=0,vmax=1,title=title, window_title=window_title, grid_lines=grid_lines, ticks=ticks)

class OctetVisualiser(BaseVisualiser):
  """
  Display 2D octet data (i.e., in the 0-255 range) as a grayscale image on a 2D grid.
  """
  def __init__(self, data, title: Optional[str] = None, window_title: Optional[str] = None, grid_lines = True, ticks = True):
      super().__init__(data, cmap='grayscale',vmin=0,vmax=255,title=title, window_title=window_title, grid_lines=grid_lines, ticks=ticks)
