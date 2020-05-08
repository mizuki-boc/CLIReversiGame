import pygame
from pygame.locals import *
import sys
import numpy as np
import readchar
import os

def main():
    #ゲーム初期化
    black = 1
    white = -1
    cells = np.zeros((8,8))
    cells[3][4] = cells[4][3] = black
    cells[3][3] = cells[4][4] = white
    turn = black
    cursorX = 0
    cursorY = 0

    #CLIゲーム処理
    while(1): cursorX,cursorY,turn = CLIdisplay(cells,turn,cursorX,cursorY)

def GUIdisplay(_cells,_turn,_cursorX = 0,_cursorY = 0):
    '''
    cellsを元に画面描画
    クリック範囲認識
    cells座標に変換
    putcheck
    cells更新
    '''
    (swidth,sheight) = (680,680)
    (cx,cy) = (100,100)
    pygame.init()
    screen = pygame.display.set_mode((swidth,sheight))
    pygame.display.set_caption("pyOthello")
    bg = pygame.image.load("/Users/mizuki/Desktop/pygameImage/pyOthelloImages/pyOthelloBoard2.png").convert_alpha()
    cursor = pygame.image.load("/Users/mizuki/Desktop/pygameImage/pyOthelloImages/pyOthelloCursor.png").convert_alpha()
    rect_bg = bg.get_rect()
    rect_cursor = cursor.get_rect()
    rect_cursor.center = (cx,cy)
    bw = 8
    bh = 8
    none = 0
    black = 1
    white = -1
    gsblack = True
    gswhite = True
    #盤面描画
    pygame.display.update()
    pygame.time.wait(30)
    screen.fill((0,0,0))
    screen.blit(bg,rect_bg)
    screen.blit(cursor,(cx,cy))

    #イベント処理
    for event in pygame.event.get():
        if event.type == MOUSEMOTION:
            cx,cy = event.pos
            cx -= int(cursor.get_width()/2)
            cy -= int(cursor.get_height()/2)
        #閉じるでquit
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


def CLIdisplay(_cells,_turn,_cursorX = 0,_cursorY = 0):
    #変数定義
    bw = 8
    bh = 8
    none = 0
    black = 1
    white = -1
    gsblack = True
    gswhite = True
    #盤面描画
    for i in range(bh):
        for j in range(bw):
            if i == _cursorY and j == _cursorX:
                print("カ",end = "")
            elif _cells[j][i] == none:
                print("・",end = "")
            elif _cells[j][i] == black:
                print("⚫️",end = "")
            elif _cells[j][i] == white:
                print("⚪️",end = "")
        print("")
    #ゲーム終了判断
    for color in [black, white]:
        for i in range(bh):
            for j in range(bw):
                gameflag = putcheck(_cells,color,j,i,False)
                if gameflag[0] == True:
                    #一箇所でも置けるところがある時,ゲームセットではない
                    if color == white:
                        gswhite = False
                    elif color == black:
                        gsblack = False
                    break
            else:
                continue
            break
    #print("black->",gsblack)
    #print("white->",gswhite)
    if gsblack == True and gswhite == False:
        _turn = white
    if gsblack == False and gswhite == True:
        _turn = black
    if gswhite == True and gsblack == True:
        print("Game Set!")
        gskey = readchar.readchar()
        pygame.quit()
        sys.exit()
    if _turn == black:
        print("black's turn")
    elif _turn == white:
        print("white's turn")

    #キー入力
    key = readchar.readchar()
    if key == "w":
        if not _cursorY - 1 < 0: _cursorY -= 1
    elif key == "a":
        if not _cursorX - 1 < 0: _cursorX -= 1
    elif key == "s":
        if not _cursorY + 1 > 7: _cursorY += 1
    elif key == "d":
        if not _cursorX + 1 > 7: _cursorX += 1
    elif key == "q":
        print("Press Q to quit game")
        quitgamekey = readchar.readchar()
        if quitgamekey == "q":
            pygame.quit()
            sys.exit()
    elif ord(key) == 13:
        #Enterキーが押されると，チェックする
        returncheck = putcheck(_cells,_turn,_cursorX,_cursorY,False)
        if returncheck[0] == True:
            #ひっくり返せる時,ひっくり返す
            putcheck(_cells,_turn,_cursorX,_cursorY,True)
            _turn = -1 * _turn
        else:
            print("can't put!")
    return _cursorX,_cursorY,_turn

#チェック関数,Trueでひっくり返す．Falseはチェックのみ
def putcheck(_cells,_turn,_x,_y,_returnflag = False):
    black = 1
    white = -1
    none = 0
    board = 8
    dirX = [-1,0,1]
    dirY = [-1,0,1]
    returncheck = False
    #選択セルに自分の石もしくは相手の石があれば，checkしない
    if _cells[_x][_y] == 1 or _cells[_x][_y] == -1:
        pass
    else:
        #check開始
        for i in dirX:
            for j in dirY:
                if _x + i >= 0 and _x + i <= 7 and _y + j >= 0 and _y + j <= 7:
                    if _cells[_x + i][_y + j] == -_turn:
                        #隣に相手の石がある時->置ける可能性
                        for n in range(2,board):
                            if _x + i * n >= 0 and _x + i * n <= 7 and _y + j * n >= 0 and _y + j * n <= 7:
                                if _cells[_x + i * n][_y + j * n] == _turn:
                                    #２個以上先に自分の石->ひっくり返す
                                    if _returnflag:
                                        #ひっくり返し処理
                                        for n2 in range(n,0,-1):
                                            _cells[_x + i * n2][_y + j * n2] = _turn
                                        _cells[_x][_y] = _turn
                                    returncheck = True
                                    break
                                elif _cells[_x + i * n][_y + j * n] == none:
                                    #２個以上先に石無し
                                    break
                    else:
                        #隣に自分の石or石なし->置けない
                        pass
    #ひっくり返せる時はTrueを返す
    return returncheck,_cells

if __name__ == '__main__':
    main()
