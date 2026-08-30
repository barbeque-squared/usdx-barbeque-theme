#!/bin/python
from pathlib import Path
import math

SRC_FOLDER='blocks'
# Default = Transparent. Colorized also works for some themes
AVATAR_FRAME_TEXTURE_TYPE='Transparent'

class ThemeWriter:
  def __init__(self):
    self.output = 'Example.ini'
    self.name = 'Example Theme'
    self.author = 'Example Author'
    # ratio = width/height. for 16:9 use 0.77
    self.avatar_ratio = 1
    # TODO: more variables

    self._outfile = None

  def write(self):
    self._outfile = open(self.output, 'w')
    
    self._writeHeader()
    self._writeBlocks()
    # custom sections
    self._writePausePopup()
    self._writeSongSelectionScreens()
    self._writeSingScreens()
    self._writeScoreScreens()
    
    self._outfile.close()
    self._outfile = None

  def _writeHeader(self):
    self._out('[Theme]\n')
    self._out('Name = '+self.name+'\n')
    self._out('BaseTheme = Modern\n')
    self._out('Creator = '+self.author+'\n')
    self._out('US_Version = USD 110\n')
    self._out('DefaultSkin = Blue\n')

  def _writeBlocks(self):
    inis = Path(SRC_FOLDER).glob('*.ini')
    for ini in sorted(inis):
      self._out('\n')
      self._out('# block: '+str(ini)+'\n')
      with open(ini, 'r') as block:
        self._out(block.read())

  def _writePausePopup(self):
    self._section('PausePopUpStatic', {'X':300, 'Y':270, 'W':200, 'H':60, 'Z':0.95, 'Tex':'Pause', 'Type':'Colorized'})

  def _writeSongSelectionScreens(self):
    self._writeSongSelectionDuetPlayers('Roulette', 535, 415)
    self._writeSongSelectionDuetPlayers('List', 553, 240)
    self._writeSongSelectionDuetPlayers('Chessboard', 310, 435)

  def _writeSongSelectionDuetPlayers(self, name: str, x: int, y: int):
    height=30
    labelWidth=154
    padding=5
    iconWidth=math.ceil(self.avatar_ratio * height)

    # text labels
    for players in ['2', '3']:
      self._section('Song'+name+'Text'+players+'PlayersDuetSingerP1', {'X':x+labelWidth-padding, 'Y':y+padding, 'Size': height-2*padding, 'Align':2, 'Color':'White'})
      self._section('Song'+name+'Text'+players+'PlayersDuetSingerP2', {'X':x+labelWidth-padding, 'Y':y+height+padding, 'Size': height-2*padding, 'Align':2, 'Color':'White'})
      self._section('Song'+name+'Text'+players+'PlayersDuetSingerP3', {'Enabled': 0})
    # player boxes
    # P1+P2: in 2P and 3P
    for players in ['2', '3']:
      self._section('Song'+name+'Static'+players+'PlayersDuetSingerP1', {'X':x+labelWidth, 'Y':y, 'W':iconWidth, 'H':height, 'Tex':'ScoreLine', 'Color':'P1Dark'})
      self._section('Song'+name+'Static'+players+'PlayersDuetSingerP2', {'X':x+labelWidth, 'Y':y+height, 'W':iconWidth, 'H':height, 'Tex':'ScoreLine', 'Color':'P2Dark'})
    # P3: in 3P and 4P
    for players in ['3', '4']:
      self._section('Song'+name+'Static'+players+'PlayersDuetSingerP3', {'X':x+labelWidth+iconWidth, 'Y':y, 'W':iconWidth, 'H':height, 'Tex':'ScoreLine', 'Color':'P3Dark'})
    # P4: in 4P and 6P
    for players in ['4', '6']:
      self._section('Song'+name+'Static'+players+'PlayersDuetSingerP4', {'X':x+labelWidth+iconWidth, 'Y':y+height, 'W':iconWidth, 'H':height, 'Tex':'ScoreLine', 'Color':'P4Dark'})
    # P5+P6: in 6P
    self._section('Song'+name+'Static6PlayersDuetSingerP5', {'X':x+labelWidth+2*iconWidth, 'Y':y, 'W':iconWidth, 'H':height, 'Tex':'ScoreLine', 'Color':'P5Dark'})
    self._section('Song'+name+'Static6PlayersDuetSingerP6', {'X':x+labelWidth+2*iconWidth, 'Y':y+height, 'W':iconWidth, 'H':height, 'Tex':'ScoreLine', 'Color':'P6Dark'})
    # P7+P8+P9: in 9P
    self._section('Song'+name+'Static9PlayersDuetSingerP7', {'X':x+labelWidth+3*iconWidth, 'Y':y, 'W':iconWidth, 'H':height, 'Tex':'ScoreLine', 'Color':'P7Dark'})
    self._section('Song'+name+'Static9PlayersDuetSingerP8', {'X':x+labelWidth+3*iconWidth, 'Y':y+height, 'W':iconWidth, 'H':height, 'Tex':'ScoreLine', 'Color':'P8Dark'})
    self._section('Song'+name+'Static9PlayersDuetSingerP9', {'X':x+labelWidth+4*iconWidth, 'Y':y, 'W':iconWidth, 'H':height, 'Tex':'ScoreLine', 'Color':'P9Dark'})

  def _writeSingScreens(self):
    yOffset=10
    offset=8
    padding=1
    # rows = oscilloscope + avatar/score
    hRow=25
    hSingBar=5
    w=80
    
    # OSCILLOSCOPE
    self._playerSections('Oscilloscope', lambda player, numPlayers: {
      'X':round(400+offset/2-(numPlayers*(offset+w))/2+(player-1)*(offset+w)+w-padding-(math.ceil(self.avatar_ratio*(hRow-2*padding)))),
      'Y':yOffset+padding, 'H':hRow-2*padding, 'W':math.ceil(self.avatar_ratio*(hRow-2*padding)),
    })

    # STATIC BACKGROUND
    self._playerSections('Static', lambda player, numPlayers: {
      'X':round(400+offset/2-(numPlayers*(offset+w))/2+(player-1)*(offset+w)),
      'Y':yOffset, 'H':hRow, 'W':w, 'Alpha':0.8, 'Tex':'ScoreLine',
      'Color':'P'+str(player)+'Dark'
    })
    # ~ # SINGBAR BACKGROUND
    # THERE IS SOMETHING SPECIAL GOING ON WITH STATIC2 WHICH MAKES IT BREAK EVERYTHING
    # ~ self._playerSections('Static2', lambda player, numPlayers: {
      # ~ 'X':round(400+offset/2-(numPlayers*(offset+w))/2+(player-1)*(offset+w)),
      # ~ 'Y':yOffset+2*hRow, 'H':2*padding+hSingBar, 'W':w, 'Alpha':0.8,
      # ~ 'Color':'Black', 'Tex':'ScoreLine'
    # ~ })
    # SINGBAR BACKGROUND
    # explicitly disable
    self._playerSections('Static2', lambda player, numPlayers: { 'Enabled': 0 })
    # PLAYER NAME
    self._playerSections('Text', lambda player, numPlayers: { 'Enabled': 0 })

    # AVATAR
    self._playerSections('Avatar', lambda player, numPlayers: {
      'X':round(400+offset/2-(numPlayers*(offset+w))/2+(player-1)*(offset+w)+padding),
      'Y':yOffset+padding, 'H':hRow-2*padding,
      'W':math.ceil(self.avatar_ratio*(hRow-2*padding))
    })

    # SCORE
    self._playerSections('TextScore', lambda player, numPlayers: {
      'X':round(400+offset/2-(numPlayers*(offset+w))/2+(player-1)*(offset+w)+padding+(math.ceil(1.2*self.avatar_ratio*(hRow-2*padding)))),
      'Y':yOffset, 'Size':hRow, 'Align':0, 'Color':'White', 'Font':0, 'Style':0,
    })

    # LINE BONUS BAR
    self._playerSections('SingBar', lambda player, numPlayers: {
      # ~ 'X':round(400+offset/2-(numPlayers*(offset+w))/2+(player-1)*(offset+w) + padding),
      'X':round(400+offset/2-(numPlayers*(offset+w))/2+(player-1)*(offset+w)),
      # ~ 'Y':yOffset+2*hRow+padding, 'W':w-2*padding, 'H':hSingBar,
      'Y':yOffset+hRow, 'W':w, 'H':hSingBar,
    })

  def _writeScoreScreens(self):
    x=20
    y=45
    h=50
    margin=10
    xNotes=320
    xLine=420
    xGolden=520
    xTotal=640
    xRating=720
    
    # table header
    # Notes
    self._sections(
      ['ScoreTextNotes1', 'ScoreTextNotes2', 'ScoreTextNotes4', 'ScoreFourPTextNotes1', 'ScoreSixPTextNotes1', 'ScoreNinePTextNotes1'],
      {'X':xNotes, 'Y':y+margin, 'Size':h-2*margin, 'Text':'SING_NOTES', 'Align':0, 'Color':'White', 'Font':0, 'Style':0}
    )
    self._disable('ScoreTextNotes', [3, 5, 6])
    self._disable('ScoreFourPTextNotes', [2, 3, 4])
    self._disable('ScoreSixPTextNotes', [2, 3, 4, 5, 6])
    # Lines
    self._sections(
      ['ScoreTextLineBonus1', 'ScoreTextLineBonus2', 'ScoreTextLineBonus4', 'ScoreFourPTextLineBonus1', 'ScoreSixPTextLineBonus1', 'ScoreNinePTextLineBonus1'],
      {'X':xLine, 'Y':y+margin, 'Size':h-2*margin, 'Text':'SING_PHRASE_BONUS', 'Align':0, 'Color':'White', 'Font':0, 'Style':0}
    )
    self._disable('ScoreTextLineBonus', [3, 5, 6])
    self._disable('ScoreFourPTextLineBonus', [2, 3, 4])
    self._disable('ScoreSixPTextLineBonus', [2, 3, 4, 5, 6])
    # Golden
    self._sections(
      ['ScoreTextGoldenNotes1', 'ScoreTextGoldenNotes2', 'ScoreTextGoldenNotes4', 'ScoreFourPTextGoldenNotes1', 'ScoreSixPTextGoldenNotes1', 'ScoreNinePTextGoldenNotes1'],
      {'X':xGolden, 'Y':y+margin, 'Size':h-2*margin, 'Text':'SING_GOLDEN_NOTES', 'Align':0, 'Color':'White', 'Font':0, 'Style':0}
    )
    self._disable('ScoreTextGoldenNotes', [3, 5, 6])
    self._disable('ScoreFourPTextGoldenNotes', [2, 3, 4])
    self._disable('ScoreSixPTextGoldenNotes', [2, 3, 4, 5, 6])
    # Total
    self._sections(
      ['ScoreTextTotal1', 'ScoreTextTotal2', 'ScoreTextTotal4', 'ScoreFourPTextTotal1', 'ScoreSixPTextTotal1', 'ScoreNinePTextTotal1'],
      {'X':xTotal, 'Y':y+margin, 'Size':h-2*margin, 'Text':'SING_TOTAL', 'Align':0, 'Color':'White', 'Font':0, 'Style':0}
    )
    self._disable('ScoreTextTotal', [3, 5, 6])
    self._disable('ScoreFourPTextTotal', [2, 3, 4])
    self._disable('ScoreSixPTextTotal', [2, 3, 4, 5, 6])
    
    # DIVIDERS
    # P1
    self._sections(
      ['ScorePlayer1Static1', 'ScorePlayer2Static1', 'ScorePlayer4Static1', 'ScoreFourPPlayer1Static1', 'ScoreSixPPlayer1Static1', 'ScoreNinePPlayer1Static1'],
      {'X':x, 'Y':y+1*h, 'W':760, 'H':1, 'Tex':'ScoreLine', 'Color':'White'}
    )
    # P2
    self._sections(
      ['ScorePlayer3Static1', 'ScorePlayer5Static1', 'ScoreFourPPlayer2Static1', 'ScoreSixPPlayer2Static1', 'ScoreNinePPlayer2Static1'],
      {'X':x, 'Y':y+2*h, 'W':760, 'H':1, 'Tex':'ScoreLine', 'Color':'White'}
    )
    # P3
    self._sections(
      ['ScorePlayer6Static1', 'ScoreFourPPlayer3Static1', 'ScoreSixPPlayer3Static1', 'ScoreNinePPlayer3Static1'],
      {'X':x, 'Y':y+3*h, 'W':760, 'H':1, 'Tex':'ScoreLine', 'Color':'White'}
    )
    # P4
    self._sections(
      ['ScoreFourPPlayer4Static1', 'ScoreSixPPlayer4Static1', 'ScoreNinePPlayer4Static1'],
      {'X':x, 'Y':y+4*h, 'W':760, 'H':1, 'Tex':'ScoreLine', 'Color':'White'}
    )
    # P5
    self._sections(
      ['ScoreSixPPlayer5Static1', 'ScoreNinePPlayer5Static1'],
      {'X':x, 'Y':y+5*h, 'W':760, 'H':1, 'Tex':'ScoreLine', 'Color':'White'}
    )
    # P6
    self._sections(
      ['ScoreSixPPlayer6Static1', 'ScoreNinePPlayer6Static1'],
      {'X':x, 'Y':y+6*h, 'W':760, 'H':1, 'Tex':'ScoreLine', 'Color':'White'}
    )
    # P7
    self._section(
      'ScoreNinePPlayer7Static1',
      {'X':x, 'Y':y+7*h, 'W':760, 'H':1, 'Tex':'ScoreLine', 'Color':'White'}
    )
    # P8
    self._section(
      'ScoreNinePPlayer8Static1',
      {'X':x, 'Y':y+8*h, 'W':760, 'H':1, 'Tex':'ScoreLine', 'Color':'White'}
    )
    # P9
    self._section(
      'ScoreNinePPlayer9Static1',
      {'X':x, 'Y':y+9*h, 'W':760, 'H':1, 'Tex':'ScoreLine', 'Color':'White'}
    )
    
    # DARKER BACKGROUNDS (for even players only)
    # NEEDS TO BE THE HIGHEST NUMBERED STATIC BECAUSE NOT EVERYONE HAS THIS!!!
    # P2
    self._sections(
      ['ScorePlayer3Static3', 'ScorePlayer5Static3', 'ScoreFourPPlayer2Static3', 'ScoreSixPPlayer2Static3', 'ScoreNinePPlayer2Static3'],
      {'X':x, 'Y':y+2*h, 'W':760, 'H':h, 'Z':0.5, 'Alpha':0.2, 'Tex':'ScoreLine', 'Color':'Black'}
    )
    # P4
    self._sections(
      ['ScoreFourPPlayer4Static3', 'ScoreSixPPlayer4Static3', 'ScoreNinePPlayer4Static3'],
      {'X':x, 'Y':y+4*h, 'W':760, 'H':h, 'Z':0.5, 'Alpha':0.2, 'Tex':'ScoreLine', 'Color':'Black'}
    )
    # P6
    self._sections(
      ['ScoreSixPPlayer6Static3', 'ScoreNinePPlayer6Static3'],
      {'X':x, 'Y':y+6*h, 'W':760, 'H':h, 'Z':0.5, 'Alpha':0.2, 'Tex':'ScoreLine', 'Color':'Black'}
    )
    # P8
    self._section(
      'ScoreNinePPlayer8Static3',
      {'X':x, 'Y':y+8*h, 'W':760, 'H':h, 'Z':0.5, 'Alpha':0.2, 'Tex':'ScoreLine', 'Color':'Black'}
    )
    # disable other statics
    self._sections(
      [
        # P1
        'ScorePlayer1Static3', 'ScorePlayer2Static3', 'ScorePlayer4Static3', 'ScoreFourPPlayer1Static3', 'ScoreSixPPlayer1Static3', 'ScoreNinePPlayer1Static3',
        # P3
        'ScorePlayer6Static3', 'ScoreFourPPlayer3Static3', 'ScoreSixPPlayer3Static3', 'ScoreNinePPlayer3Static3',
        # P5
        'ScoreSixPPlayer5Static3', 'ScoreNinePPlayer5Static3',
        # P7
        'ScoreNinePPlayer7Static3',
        # P9
        'ScoreNinePPlayer9Static3'
      ],
      { 'Enabled': 0 }
    )
    
    # AVATARS
    # P1
    self._sections(
      ['ScorePlayer1Avatar', 'ScorePlayer2Avatar', 'ScorePlayer4Avatar', 'ScoreFourPPlayer1Avatar', 'ScoreSixPPlayer1Avatar', 'ScoreNinePPlayer1Avatar'],
      {'X':x+round(margin/2), 'Y':y+1*h+round(margin/2), 'W':math.ceil(self.avatar_ratio*(h-margin)), 'H':h-margin}
    )
    # P2
    self._sections(
      ['ScorePlayer3Avatar', 'ScorePlayer5Avatar', 'ScoreFourPPlayer2Avatar', 'ScoreSixPPlayer2Avatar', 'ScoreNinePPlayer2Avatar'],
      {'X':x+round(margin/2), 'Y':y+2*h+round(margin/2), 'W':math.ceil(self.avatar_ratio*(h-margin)), 'H':h-margin, 'Z':1}
    )
    # P3
    self._sections(
      ['ScorePlayer6Avatar', 'ScoreFourPPlayer3Avatar', 'ScoreSixPPlayer3Avatar', 'ScoreNinePPlayer3Avatar'],
      {'X':x+round(margin/2), 'Y':y+3*h+round(margin/2), 'W':math.ceil(self.avatar_ratio*(h-margin)), 'H':h-margin}
    )
    # P4
    self._sections(
      ['ScoreFourPPlayer4Avatar', 'ScoreSixPPlayer4Avatar', 'ScoreNinePPlayer4Avatar'],
      {'X':x+round(margin/2), 'Y':y+4*h+round(margin/2), 'W':math.ceil(self.avatar_ratio*(h-margin)), 'H':h-margin, 'Z':1}
    )
    # P5
    self._sections(
      ['ScoreSixPPlayer5Avatar', 'ScoreNinePPlayer5Avatar'],
      {'X':x+round(margin/2), 'Y':y+5*h+round(margin/2), 'W':math.ceil(self.avatar_ratio*(h-margin)), 'H':h-margin}
    )
    # P6
    self._sections(
      ['ScoreSixPPlayer6Avatar', 'ScoreNinePPlayer6Avatar'],
      {'X':x+round(margin/2), 'Y':y+6*h+round(margin/2), 'W':math.ceil(self.avatar_ratio*(h-margin)), 'H':h-margin, 'Z':1}
    )
    # P7
    self._section(
      'ScoreNinePPlayer7Avatar',
      {'X':x+round(margin/2), 'Y':y+7*h+round(margin/2), 'W':math.ceil(self.avatar_ratio*(h-margin)), 'H':h-margin, 'Z':1}
    )
    # P8
    self._section(
      'ScoreNinePPlayer8Avatar',
      {'X':x+round(margin/2), 'Y':y+8*h+round(margin/2), 'W':math.ceil(self.avatar_ratio*(h-margin)), 'H':h-margin, 'Z':1}
    )
    # P9
    self._section(
      'ScoreNinePPlayer9Avatar',
      {'X':x+round(margin/2), 'Y':y+9*h+round(margin/2), 'W':math.ceil(self.avatar_ratio*(h-margin)), 'H':h-margin, 'Z':1}
    )
    
    # AVATAR FRAMES
    # P1
    self._sections(
      ['ScorePlayer1Static2', 'ScorePlayer2Static2', 'ScorePlayer4Static2', 'ScoreFourPPlayer1Static2', 'ScoreSixPPlayer1Static2', 'ScoreNinePPlayer1Static2'],
      {'X':x+round(margin/2)-round(margin/4), 'Y':y+1*h+round(margin/2)-round(margin/4), 'W':math.ceil(self.avatar_ratio*(h-margin))+round(margin/2), 'H':h-margin+round(margin/2), 'Tex':'AvatarFrame2', 'Color':'P1Dark', 'Type':AVATAR_FRAME_TEXTURE_TYPE}
    )
    # P2
    self._sections(
      ['ScorePlayer3Static2', 'ScorePlayer5Static2', 'ScoreFourPPlayer2Static2', 'ScoreSixPPlayer2Static2', 'ScoreNinePPlayer2Static2'],
      {'X':x+round(margin/2)-round(margin/4), 'Y':y+2*h+round(margin/2)-round(margin/4), 'W':math.ceil(self.avatar_ratio*(h-margin))+round(margin/2), 'H':h-margin+round(margin/2), 'Tex':'AvatarFrame2', 'Color':'P2Dark', 'Type':AVATAR_FRAME_TEXTURE_TYPE, 'Z':0.9}
    )
    # P3
    self._sections(
      ['ScorePlayer6Static2', 'ScoreFourPPlayer3Static2', 'ScoreSixPPlayer3Static2', 'ScoreNinePPlayer3Static2'],
      {'X':x+round(margin/2)-round(margin/4), 'Y':y+3*h+round(margin/2)-round(margin/4), 'W':math.ceil(self.avatar_ratio*(h-margin))+round(margin/2), 'H':h-margin+round(margin/2), 'Tex':'AvatarFrame2', 'Color':'P3Dark', 'Type':AVATAR_FRAME_TEXTURE_TYPE}
    )
    # P4
    self._sections(
      ['ScoreFourPPlayer4Static2', 'ScoreSixPPlayer4Static2', 'ScoreNinePPlayer4Static2'],
      {'X':x+round(margin/2)-round(margin/4), 'Y':y+4*h+round(margin/2)-round(margin/4), 'W':math.ceil(self.avatar_ratio*(h-margin))+round(margin/2), 'H':h-margin+round(margin/2), 'Tex':'AvatarFrame2', 'Color':'P4Dark', 'Type':AVATAR_FRAME_TEXTURE_TYPE, 'Z':0.9}
    )
    # P5
    self._sections(
      ['ScoreSixPPlayer5Static2', 'ScoreNinePPlayer5Static2'],
      {'X':x+round(margin/2)-round(margin/4), 'Y':y+5*h+round(margin/2)-round(margin/4), 'W':math.ceil(self.avatar_ratio*(h-margin))+round(margin/2), 'H':h-margin+round(margin/2), 'Tex':'AvatarFrame2', 'Color':'P5Dark', 'Type':AVATAR_FRAME_TEXTURE_TYPE}
    )
    # P6
    self._sections(
      ['ScoreSixPPlayer6Static2', 'ScoreNinePPlayer6Static2'],
      {'X':x+round(margin/2)-round(margin/4), 'Y':y+6*h+round(margin/2)-round(margin/4), 'W':math.ceil(self.avatar_ratio*(h-margin))+round(margin/2), 'H':h-margin+round(margin/2), 'Tex':'AvatarFrame2', 'Color':'P6Dark', 'Type':AVATAR_FRAME_TEXTURE_TYPE, 'Z':0.9}
    )
    # P7
    self._sections(
      ['ScoreNinePPlayer7Static2'],
      {'X':x+round(margin/2)-round(margin/4), 'Y':y+7*h+round(margin/2)-round(margin/4), 'W':math.ceil(self.avatar_ratio*(h-margin))+round(margin/2), 'H':h-margin+round(margin/2), 'Tex':'AvatarFrame2', 'Color':'P7Dark', 'Type':AVATAR_FRAME_TEXTURE_TYPE, 'Z':0.9}
    )
    # P8
    self._sections(
      ['ScoreNinePPlayer8Static2'],
      {'X':x+round(margin/2)-round(margin/4), 'Y':y+8*h+round(margin/2)-round(margin/4), 'W':math.ceil(self.avatar_ratio*(h-margin))+round(margin/2), 'H':h-margin+round(margin/2), 'Tex':'AvatarFrame2', 'Color':'P8Dark', 'Type':AVATAR_FRAME_TEXTURE_TYPE, 'Z':0.9}
    )
    # P9
    self._sections(
      ['ScoreNinePPlayer9Static2'],
      {'X':x+round(margin/2)-round(margin/4), 'Y':y+9*h+round(margin/2)-round(margin/4), 'W':math.ceil(self.avatar_ratio*(h-margin))+round(margin/2), 'H':h-margin+round(margin/2), 'Tex':'AvatarFrame2', 'Color':'P9Dark', 'Type':AVATAR_FRAME_TEXTURE_TYPE, 'Z':0.9}
    )
    
    # NAMES
    # P1
    self._sections(
      ['ScoreTextName1', 'ScoreTextName2', 'ScoreTextName4', 'ScoreFourPTextName1', 'ScoreSixPTextName1', 'ScoreNinePTextName1'],
      {'X':x+h, 'Y':y+1*h+round(margin/2), 'Size':h-margin, 'Text':'P1', 'Color':'White', 'Font':0, 'Style':1}
    )
    # P2
    self._sections(
      ['ScoreTextName3', 'ScoreTextName5', 'ScoreFourPTextName2', 'ScoreSixPTextName2', 'ScoreNinePTextName2'],
      {'X':x+h, 'Y':y+2*h+round(margin/2), 'Size':h-margin, 'Text':'P2', 'Color':'White', 'Font':0, 'Style':1}
    )
    # P3
    self._sections(
      ['ScoreTextName6', 'ScoreFourPTextName3', 'ScoreSixPTextName3', 'ScoreNinePTextName3'],
      {'X':x+h, 'Y':y+3*h+round(margin/2), 'Size':h-margin, 'Text':'P3', 'Color':'White', 'Font':0, 'Style':1}
    )
    # P4
    self._sections(
      ['ScoreFourPTextName4', 'ScoreSixPTextName4', 'ScoreNinePTextName4'],
      {'X':x+h, 'Y':y+4*h+round(margin/2), 'Size':h-margin, 'Text':'P4', 'Color':'White', 'Font':0, 'Style':1}
    )
    # P5
    self._sections(
      ['ScoreSixPTextName5', 'ScoreNinePTextName5'],
      {'X':x+h, 'Y':y+5*h+round(margin/2), 'Size':h-margin, 'Text':'P5', 'Color':'White', 'Font':0, 'Style':1}
    )
    # P6
    self._sections(
      ['ScoreSixPTextName6', 'ScoreNinePTextName6'],
      {'X':x+h, 'Y':y+6*h+round(margin/2), 'Size':h-margin, 'Text':'P6', 'Color':'White', 'Font':0, 'Style':1}
    )
    # P7
    self._sections(
      ['ScoreNinePTextName7'],
      {'X':x+h, 'Y':y+7*h+round(margin/2), 'Size':h-margin, 'Text':'P6', 'Color':'White', 'Font':0, 'Style':1}
    )
    # P8
    self._sections(
      ['ScoreNinePTextName8'],
      {'X':x+h, 'Y':y+8*h+round(margin/2), 'Size':h-margin, 'Text':'P6', 'Color':'White', 'Font':0, 'Style':1}
    )
    # P9
    self._sections(
      ['ScoreNinePTextName9'],
      {'X':x+h, 'Y':y+9*h+round(margin/2), 'Size':h-margin, 'Text':'P6', 'Color':'White', 'Font':0, 'Style':1}
    )
    
    # NOTE SCORES
    # P1
    self._sections(
      ['ScoreTextNotesScore1', 'ScoreTextNotesScore2', 'ScoreTextNotesScore4', 'ScoreFourPTextNotesScore1', 'ScoreSixPTextNotesScore1', 'ScoreNinePTextNotesScore1'],
      {'X':xNotes, 'Y':y+1*h+margin, 'Size':h-2*margin, 'Text':'0', 'Color':'White', 'Font':0, 'Style':0}
    )
    # P2
    self._sections(
      ['ScoreTextNotesScore3', 'ScoreTextNotesScore5', 'ScoreFourPTextNotesScore2', 'ScoreSixPTextNotesScore2', 'ScoreNinePTextNotesScore2'],
      {'X':xNotes, 'Y':y+2*h+margin, 'Size':h-2*margin, 'Text':'0', 'Color':'White', 'Font':0, 'Style':0}
    )
    # P3
    self._sections(
      ['ScoreTextNotesScore6', 'ScoreFourPTextNotesScore3', 'ScoreSixPTextNotesScore3', 'ScoreNinePTextNotesScore3'],
      {'X':xNotes, 'Y':y+3*h+margin, 'Size':h-2*margin, 'Text':'0', 'Color':'White', 'Font':0, 'Style':0}
    )
    # P4
    self._sections(
      ['ScoreFourPTextNotesScore4', 'ScoreSixPTextNotesScore4', 'ScoreNinePTextNotesScore4'],
      {'X':xNotes, 'Y':y+4*h+margin, 'Size':h-2*margin, 'Text':'0', 'Color':'White', 'Font':0, 'Style':0}
    )
    # P5
    self._sections(
      ['ScoreSixPTextNotesScore5', 'ScoreNinePTextNotesScore5'],
      {'X':xNotes, 'Y':y+5*h+margin, 'Size':h-2*margin, 'Text':'0', 'Color':'White', 'Font':0, 'Style':0}
    )
    # P6
    self._sections(
      ['ScoreSixPTextNotesScore6', 'ScoreNinePTextNotesScore6'],
      {'X':xNotes, 'Y':y+6*h+margin, 'Size':h-2*margin, 'Text':'0', 'Color':'White', 'Font':0, 'Style':0}
    )
    # P7
    self._sections(
      ['ScoreNinePTextNotesScore7'],
      {'X':xNotes, 'Y':y+7*h+margin, 'Size':h-2*margin, 'Text':'0', 'Color':'White', 'Font':0, 'Style':0}
    )
    # P8
    self._sections(
      ['ScoreNinePTextNotesScore8'],
      {'X':xNotes, 'Y':y+8*h+margin, 'Size':h-2*margin, 'Text':'0', 'Color':'White', 'Font':0, 'Style':0}
    )
    # P9
    self._sections(
      ['ScoreNinePTextNotesScore9'],
      {'X':xNotes, 'Y':y+9*h+margin, 'Size':h-2*margin, 'Text':'0', 'Color':'White', 'Font':0, 'Style':0}
    )
    
    # LINE SCORES
    # P1
    self._sections(
      ['ScoreTextLineBonusScore1', 'ScoreTextLineBonusScore2', 'ScoreTextLineBonusScore4', 'ScoreFourPTextLineBonusScore1', 'ScoreSixPTextLineBonusScore1', 'ScoreNinePTextLineBonusScore1'],
      {'X':xLine, 'Y':y+1*h+margin, 'Size':h-2*margin, 'Text':'0', 'Color':'White', 'Font':0, 'Style':0}
    )
    # P2
    self._sections(
      ['ScoreTextLineBonusScore3', 'ScoreTextLineBonusScore5', 'ScoreFourPTextLineBonusScore2', 'ScoreSixPTextLineBonusScore2', 'ScoreNinePTextLineBonusScore2'],
      {'X':xLine, 'Y':y+2*h+margin, 'Size':h-2*margin, 'Text':'0', 'Color':'White', 'Font':0, 'Style':0}
    )
    # P3
    self._sections(
      ['ScoreTextLineBonusScore6', 'ScoreFourPTextLineBonusScore3', 'ScoreSixPTextLineBonusScore3', 'ScoreNinePTextLineBonusScore3'],
      {'X':xLine, 'Y':y+3*h+margin, 'Size':h-2*margin, 'Text':'0', 'Color':'White', 'Font':0, 'Style':0}
    )
    # P4
    self._sections(
      ['ScoreFourPTextLineBonusScore4', 'ScoreSixPTextLineBonusScore4', 'ScoreNinePTextLineBonusScore4'],
      {'X':xLine, 'Y':y+4*h+margin, 'Size':h-2*margin, 'Text':'0', 'Color':'White', 'Font':0, 'Style':0}
    )
    # P5
    self._sections(
      ['ScoreSixPTextLineBonusScore5', 'ScoreNinePTextLineBonusScore5'],
      {'X':xLine, 'Y':y+5*h+margin, 'Size':h-2*margin, 'Text':'0', 'Color':'White', 'Font':0, 'Style':0}
    )
    # P6
    self._sections(
      ['ScoreSixPTextLineBonusScore6', 'ScoreNinePTextLineBonusScore6'],
      {'X':xLine, 'Y':y+6*h+margin, 'Size':h-2*margin, 'Text':'0', 'Color':'White', 'Font':0, 'Style':0}
    )
    # P7
    self._sections(
      ['ScoreNinePTextLineBonusScore7'],
      {'X':xLine, 'Y':y+7*h+margin, 'Size':h-2*margin, 'Text':'0', 'Color':'White', 'Font':0, 'Style':0}
    )
    # P8
    self._sections(
      ['ScoreNinePTextLineBonusScore8'],
      {'X':xLine, 'Y':y+8*h+margin, 'Size':h-2*margin, 'Text':'0', 'Color':'White', 'Font':0, 'Style':0}
    )
    # P9
    self._sections(
      ['ScoreNinePTextLineBonusScore9'],
      {'X':xLine, 'Y':y+9*h+margin, 'Size':h-2*margin, 'Text':'0', 'Color':'White', 'Font':0, 'Style':0}
    )
    
    # GOLDEN SCORES
    # P1
    self._sections(
      ['ScoreTextGoldenNotesScore1', 'ScoreTextGoldenNotesScore2', 'ScoreTextGoldenNotesScore4', 'ScoreFourPTextGoldenNotesScore1', 'ScoreSixPTextGoldenNotesScore1', 'ScoreNinePTextGoldenNotesScore1'],
      {'X':xGolden, 'Y':y+1*h+margin, 'Size':h-2*margin, 'Text':'0', 'Color':'White', 'Font':0, 'Style':0}
    )
    # P2
    self._sections(
      ['ScoreTextGoldenNotesScore3', 'ScoreTextGoldenNotesScore5', 'ScoreFourPTextGoldenNotesScore2', 'ScoreSixPTextGoldenNotesScore2', 'ScoreNinePTextGoldenNotesScore2'],
      {'X':xGolden, 'Y':y+2*h+margin, 'Size':h-2*margin, 'Text':'0', 'Color':'White', 'Font':0, 'Style':0}
    )
    # P3
    self._sections(
      ['ScoreTextGoldenNotesScore6', 'ScoreFourPTextGoldenNotesScore3', 'ScoreSixPTextGoldenNotesScore3', 'ScoreNinePTextGoldenNotesScore3'],
      {'X':xGolden, 'Y':y+3*h+margin, 'Size':h-2*margin, 'Text':'0', 'Color':'White', 'Font':0, 'Style':0}
    )
    # P4
    self._sections(
      ['ScoreFourPTextGoldenNotesScore4', 'ScoreSixPTextGoldenNotesScore4', 'ScoreNinePTextGoldenNotesScore4'],
      {'X':xGolden, 'Y':y+4*h+margin, 'Size':h-2*margin, 'Text':'0', 'Color':'White', 'Font':0, 'Style':0}
    )
    # P5
    self._sections(
      ['ScoreSixPTextGoldenNotesScore5', 'ScoreNinePTextGoldenNotesScore5'],
      {'X':xGolden, 'Y':y+5*h+margin, 'Size':h-2*margin, 'Text':'0', 'Color':'White', 'Font':0, 'Style':0}
    )
    # P6
    self._sections(
      ['ScoreSixPTextGoldenNotesScore6', 'ScoreNinePTextGoldenNotesScore6'],
      {'X':xGolden, 'Y':y+6*h+margin, 'Size':h-2*margin, 'Text':'0', 'Color':'White', 'Font':0, 'Style':0}
    )
    # P7
    self._sections(
      ['ScoreNinePTextGoldenNotesScore7'],
      {'X':xGolden, 'Y':y+7*h+margin, 'Size':h-2*margin, 'Text':'0', 'Color':'White', 'Font':0, 'Style':0}
    )
    # P8
    self._sections(
      ['ScoreNinePTextGoldenNotesScore8'],
      {'X':xGolden, 'Y':y+8*h+margin, 'Size':h-2*margin, 'Text':'0', 'Color':'White', 'Font':0, 'Style':0}
    )
    # P9
    self._sections(
      ['ScoreNinePTextGoldenNotesScore9'],
      {'X':xGolden, 'Y':y+9*h+margin, 'Size':h-2*margin, 'Text':'0', 'Color':'White', 'Font':0, 'Style':0}
    )
    
    # TOTAL SCORES
    # P1
    self._sections(
      ['ScoreTextTotalScore1', 'ScoreTextTotalScore2', 'ScoreTextTotalScore4', 'ScoreFourPTextTotalScore1', 'ScoreSixPTextTotalScore1', 'ScoreNinePTextTotalScore1'],
      {'X':xTotal, 'Y':y+1*h+round(margin/2), 'Size':h-margin, 'Text':'0', 'Color':'White', 'Font':0, 'Style':0}
    )
    # P2
    self._sections(
      ['ScoreTextTotalScore3', 'ScoreTextTotalScore5', 'ScoreFourPTextTotalScore2', 'ScoreSixPTextTotalScore2', 'ScoreNinePTextTotalScore2'],
      {'X':xTotal, 'Y':y+2*h+round(margin/2), 'Size':h-margin, 'Text':'0', 'Color':'White', 'Font':0, 'Style':0}
    )
    # P3
    self._sections(
      ['ScoreTextTotalScore6', 'ScoreFourPTextTotalScore3', 'ScoreSixPTextTotalScore3', 'ScoreNinePTextTotalScore3'],
      {'X':xTotal, 'Y':y+3*h+round(margin/2), 'Size':h-margin, 'Text':'0', 'Color':'White', 'Font':0, 'Style':0}
    )
    # P4
    self._sections(
      ['ScoreFourPTextTotalScore4', 'ScoreSixPTextTotalScore4', 'ScoreNinePTextTotalScore4'],
      {'X':xTotal, 'Y':y+4*h+round(margin/2), 'Size':h-margin, 'Text':'0', 'Color':'White', 'Font':0, 'Style':0}
    )
    # P5
    self._sections(
      ['ScoreSixPTextTotalScore5', 'ScoreNinePTextTotalScore5'],
      {'X':xTotal, 'Y':y+5*h+round(margin/2), 'Size':h-margin, 'Text':'0', 'Color':'White', 'Font':0, 'Style':0}
    )
    # P6
    self._sections(
      ['ScoreSixPTextTotalScore6', 'ScoreNinePTextTotalScore6'],
      {'X':xTotal, 'Y':y+6*h+round(margin/2), 'Size':h-margin, 'Text':'0', 'Color':'White', 'Font':0, 'Style':0}
    )
    # P7
    self._sections(
      ['ScoreNinePTextTotalScore7'],
      {'X':xTotal, 'Y':y+7*h+round(margin/2), 'Size':h-margin, 'Text':'0', 'Color':'White', 'Font':0, 'Style':0}
    )
    # P8
    self._sections(
      ['ScoreNinePTextTotalScore8'],
      {'X':xTotal, 'Y':y+8*h+round(margin/2), 'Size':h-margin, 'Text':'0', 'Color':'White', 'Font':0, 'Style':0}
    )
    # P9
    self._sections(
      ['ScoreNinePTextTotalScore9'],
      {'X':xTotal, 'Y':y+9*h+round(margin/2), 'Size':h-margin, 'Text':'0', 'Color':'White', 'Font':0, 'Style':0}
    )
    
    # DISABLE ALL OTHER TEXTS AND STATICS: Score...Text1, Score...Static4-6
    self._scoreSections('Text1', { 'Enabled': 0 })
    self._scoreSections('Static4', { 'Enabled': 0 })
    self._scoreSections('Static5', { 'Enabled': 0 })
    self._scoreSections('Static6', { 'Enabled': 0 })
    # 3 and 4 players also have a Static7 and Static8 -- but just nuke them for all players
    self._scoreSections('Static7', { 'Enabled': 0 })
    self._scoreSections('Static8', { 'Enabled': 0 })
    # rating picture
    self._disable('ScoreStaticRatingPicture', [1, 2, 3, 4, 5, 6])
    self._disable('ScoreFourPStaticRatingPicture', [1, 2, 3, 4])
    # rating text (tone deaf etc)
    self._disable('ScoreTextScore', [1, 2, 3, 4, 5, 6])
    self._disable('ScoreFourPTextScore', [1, 2, 3, 4])
    # rating box (notes)
    self._disable('ScoreStaticBoxDark', [1, 2, 3, 4, 5, 6])
    self._disable('ScoreFourPStaticBoxDark', [1, 2, 3, 4])
    # rating box (line)
    self._disable('ScoreStaticBoxLight', [1, 2, 3, 4, 5, 6])
    self._disable('ScoreFourPStaticBoxLight', [1, 2, 3, 4])
    # rating box (golden)
    self._disable('ScoreStaticBoxLightest', [1, 2, 3, 4, 5, 6])
    self._disable('ScoreFourPStaticBoxLightest', [1, 2, 3, 4])
    # the bar thing
    self._disable('ScoreStaticBackLevel', [1, 2, 3, 4, 5, 6])
    self._disable('ScoreFourPStaticBackLevel', [1, 2, 3, 4])
    self._disable('ScoreStaticBackLevelRound', [1, 2, 3, 4, 5, 6])
    self._disable('ScoreFourPStaticBackLevelRound', [1, 2, 3, 4])
    self._disable('ScoreStaticLevel', [1, 2, 3, 4, 5, 6])
    self._disable('ScoreFourPStaticLevel', [1, 2, 3, 4])
    self._disable('ScoreStaticLevelRound', [1, 2, 3, 4, 5, 6])
    self._disable('ScoreFourPStaticLevelRound', [1, 2, 3, 4])

  def _out(self, string):
    self._outfile.write(string)
  
  def _disable(self, name, players):
    for player in players:
      self._section(name+str(player), {'Enabled': 0})
  
  def _playerSections(self, name, f):
    sections = [
      # 1 player
      [
        ['P1'],
      ],
      # 2 players
      [
        ['P1TwoP'],
        ['P2R'],
      ],
      # 3 players
      [
        ['P1ThreeP', 'DuetP1ThreeP'],
        ['P2M', 'DuetP2M'],
        ['P3R', 'DuetP3R'],
      ],
      # 4 players
      [
        ['P1FourP', 'P1DuetFourP'],
        ['P2FourP', 'P2DuetFourP'],
        ['P3FourP', 'P3DuetFourP'],
        ['P4FourP', 'P4DuetFourP'],
      ],
      # 5 players
      [],
      # 6 players
      [
        ['P1SixP', 'P1DuetSixP'],
        ['P2SixP', 'P2DuetSixP'],
        ['P3SixP', 'P3DuetSixP'],
        ['P4SixP', 'P4DuetSixP'],
        ['P5SixP', 'P5DuetSixP'],
        ['P6SixP', 'P6DuetSixP'],
      ],
      # 7 players
      [],
      # 8 players
      [],
      # 9 players
      [
        ['P1NineP', 'P1DuetNineP'],
        ['P2NineP', 'P2DuetNineP'],
        ['P3NineP', 'P3DuetNineP'],
        ['P4NineP', 'P4DuetNineP'],
        ['P5NineP', 'P5DuetNineP'],
        ['P6NineP', 'P6DuetNineP'],
        ['P7NineP', 'P7DuetNineP'],
        ['P8NineP', 'P8DuetNineP'],
        ['P9NineP', 'P9DuetNineP'],
      ],
    ]
    for numPlayers, players in enumerate(sections, start=1):
      for player, sectionNames in enumerate(players, start=1):
        for sectionName in sectionNames:
          fullSectionName = 'Sing'+sectionName+name
          # a weird edge case
          if fullSectionName == 'SingP3RSingBar':
            fullSectionName = 'SingP3SingBar'
          self._section(fullSectionName, f(player, numPlayers))

  def _scoreSections(self, name, values):
    sections = [
      # P1
      'Player1', 'Player2', 'Player4', 'FourPPlayer1', 'SixPPlayer1', 'NinePPlayer1',
      # P2
      'Player3', 'Player5', 'FourPPlayer2', 'SixPPlayer2', 'NinePPlayer2',
      # P3
      'Player6', 'FourPPlayer3', 'SixPPlayer3', 'NinePPlayer3',
      # P4
      'FourPPlayer4', 'SixPPlayer4', 'NinePPlayer4',
      # P5
      'SixPPlayer5', 'NinePPlayer5',
      # P6
      'SixPPlayer6', 'NinePPlayer6',
      # P7
      'NinePPlayer7',
      # P8
      'NinePPlayer8',
      # P9
      'NinePPlayer9',
    ]
    for sectionName in sections:
      fullSectionName = 'Score'+sectionName+name
      self._section(fullSectionName, values)
  
  def _sections(self, headers, values):
    for i in headers:
      self._section(i, values)

  def _section(self, header, values):
    res = '\n'
    res += '['+header+']\n'
    for key, value in values.items():
      res += key+' = '+str(value)+'\n'
    self._out(res)

w = ThemeWriter()
# 4:3
w.output = 'barbeque.one-Normal.ini'
w.name = 'barbeque.one-Normal'
w.author = 'barbeque'
w.avatar_ratio = 1
w.write()
# 16:9
w.output = 'barbeque.one-Widescreen.ini'
w.name = 'barbeque.one-Widescreen'
w.author = 'barbeque'
w.avatar_ratio = 0.77
w.write()
