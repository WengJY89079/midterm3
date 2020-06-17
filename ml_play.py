from os import path
import pickle

def whatLane(playerX : int):
    if playerX < 70:
        return (0, playerX)
    elif playerX < 140:
        return (1 , playerX - 70)
    elif playerX < 210:
        return (2, playerX - 140)
    elif playerX < 280:
        return (3, playerX - 210)
    elif playerX < 350:
        return (4, playerX - 280)
    elif playerX < 420:
        return (5, playerX - 350)
    elif playerX < 490:
        return (6, playerX - 420)
    elif playerX < 560:
        return (7, playerX - 490)
    else:
        return (8, playerX - 560)

class MLPlay:
    def __init__(self, player):
        self.player = player
        with open(path.join(path.dirname(__file__), 'tree1.pickle'), 'rb') as f:
            self.tree = pickle.load(f)
        if self.player == "player1":
            self.player_no = 0
        elif self.player == "player2":
            self.player_no = 1
        elif self.player == "player3":
            self.player_no = 2
        elif self.player == "player4":
            self.player_no = 3
        self.car_vel = 0
        self.car_pos = ()
        pass

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        playerLane = -10000
        playerLaneLeft = -10000
        playerX = -10000
        playerY = -10000
        forward = -10000
        back = -10000
        forward_left = -10000
        forward_left_left = -10000
        forward_right = -10000
        forward_right_right = -10000
        back_left = -10000
        back_left_left = -10000
        back_right = -10000
        back_right_right = -10000
        left = -10000
        left_left = -10000
        right = -10000
        right_right = -10000

        self.car_pos = scene_info[self.player]
        for car in scene_info["cars_info"]:
            if car["id"]==self.player_no:
                self.car_vel = car["velocity"]
                if car['id'] == self.player_no:
                    playerLane, playerLaneLeft = whatLane(playerX=car['pos'][0])
                    playerX = car['pos'][0]
                    playerY = car['pos'][1]
                    forward = playerY
                    back = 800 - playerY
                    if playerLane != 0:
                        back_left = back
                        forward_left = forward
                    if playerLane != 8:
                        back_right = back
                        forward_right = forward
                    if playerLane != 1 and playerLane != 0:
                        back_left_left = back
                        forward_left_left = forward
                    if playerLane != 8 and playerLane != 7:
                        back_right_right = back
                        forward_right_right = forward
        for car in scene_info["cars_info"]:
            if car['id'] != self.player_no:
                carLane, carLaneLeft = whatLane(playerX=car['pos'][0])
                carX = car['pos'][0]
                carY = car['pos'][1]
                if carLane == playerLane:
                    if carY > playerY:
                        if back > carY - playerY - 80 and abs(playerX - carX) <= 40:
                            back = carY - playerY - 80
                        if carLaneLeft < 10:
                            if back_left > carY - playerY - 80:
                                back_left = carY - playerY - 80
                        if carLaneLeft > 60:
                            if back_right > carY - playerY - 80:
                                back_right = carY - playerY - 80
                    else:
                        if forward > playerY - carY - 80 and abs(playerX - carX) <= 40:
                            forward = playerY - carY - 80
                        if carLaneLeft < 10:
                            if forward_left > playerY - carY - 80:
                                forward_left = playerY - carY - 80
                        if carLaneLeft > 60:
                            if forward_right > playerY - carY - 80:
                                forward_right = playerY - carY - 80
                    if abs(carY - playerY) - 80 <= 0:
                        if carX > playerX:
                            if right == -10000 or right > carLaneLeft - playerLaneLeft:
                                right = carLaneLeft - playerLaneLeft
                        else:
                            if left == -10000 or left > playerLaneLeft - carLaneLeft:
                                left = playerLaneLeft - carLaneLeft
                if carLane == playerLane - 1 and playerLane != 0:
                    if carY > playerY:
                        if playerLaneLeft - carLaneLeft + 70 <= 40:
                            if back > carY - playerY - 80:
                                back = carY - playerY - 80
                        if carLaneLeft < 10:
                            if back_left_left > carY - playerY - 80:
                                back_left_left = carY - playerY - 80
                        if back_left > carY - playerY - 80:
                            back_left = carY - playerY - 80
                    else:
                        if playerLaneLeft - carLaneLeft + 70 <= 40:
                            if forward > playerY - carY - 80:
                                forward = playerY - carY - 80
                        if carLaneLeft < 10:
                            if forward_left_left > playerY - carY - 80:
                                forward_left_left = playerY - carY - 80
                        if forward_left > playerY - carY - 80:
                            forward_left = playerY - carY - 80
                    if ((forward_left < 20 and forward_left != -10000) or (back_left < 20 and back_left != -10000))  and abs(carY - playerY) - 80 <= 0:
                        if left == -10000 or left > playerLaneLeft - carLaneLeft + 70:
                            left = playerLaneLeft - carLaneLeft + 70
                if carLane == playerLane + 1 and playerLane != 8:
                    if carY > playerY:
                        if carLaneLeft - playerLaneLeft + 70 <= 40:
                            if back > carY - playerY - 80:
                                back = carY - playerY - 80
                        if carLaneLeft > 60:
                            if back_right_right > carY - playerY - 80:
                                back_right_right = carY - playerY - 80
                        if back_right > carY - playerY - 80:
                            back_right = carY - playerY - 80
                    else:
                        if carLaneLeft - playerLaneLeft + 70 <= 40:
                            if forward > playerY - carY - 80:
                                forward = playerY - carY - 80
                        if carLaneLeft > 60:
                            if forward_right_right > playerY - carY - 80:
                                forward_right_right = playerY - carY - 80
                        if forward_right > playerY - carY - 80:
                            forward_right = playerY - carY - 80
                    if ((forward_right < 20 and forward_right != -10000) or(back_right < 20 and back_right != -10000))  and abs(carY - playerY) - 80 <= 0:
                            right = carLaneLeft - playerLaneLeft + 70
                if carLane == playerLane - 2 and playerLane > 1:
                    if carY > playerY:
                        if back_left_left > carY - playerY - 80:
                            back_left_left = carY - playerY - 80
                        if carLaneLeft > 60:
                            if back_left > carY - playerY - 80:
                                back_left = carY - playerY - 80
                    else:
                        if forward_left_left > playerY - carY - 80:
                            forward_left_left = playerY - carY - 80
                        if carLaneLeft > 60:
                            if forward_left > playerY - carY - 80:
                                forward_left = playerY - carY - 80
                    if ((forward_left_left < 20 and forward_left_left != -10000) or (back_left_left < 20 and back_left_left != -10000))  and abs(carY - playerY) - 80 <= 0:
                        if left_left == -10000 or left_left > playerLaneLeft - carLaneLeft + 140:
                            left_left = playerLaneLeft - carLaneLeft + 140
                if carLane == playerLane + 2 and playerLane < 7:
                    if carY > playerY:
                        if back_right_right > carY - playerY - 80:
                            back_right_right = carY - playerY - 80
                        if carLaneLeft < 10:
                            if back_right > carY - playerY - 80:
                                back_right = carY - playerY - 80
                    else:
                        if forward_right_right > playerY - carY - 80:
                            forward_right_right = playerY - carY - 80
                        if carLaneLeft < 10:
                            if forward_right > playerY - carY - 80:
                                forward_right = playerY - carY - 80
                    if ((forward_right_right < 20 and forward_right_right != -10000) or(back_right_right < 20 and back_right_right != -10000))  and abs(carY - playerY) - 80 <= 0:
                        if right_right == -10000 or right_right > carLaneLeft - playerLaneLeft + 140:
                            right_right = carLaneLeft - playerLaneLeft + 140


        if scene_info["status"] != "ALIVE":
            return "RESET"


        feature = [[forward, back, left, left_left, right, right_right, forward_left, forward_right, back_left, back_right, forward_left_left, forward_right_right, back_left_left, back_right_right, playerLaneLeft, playerLane]]

        pred = self.tree.predict(feature)

        if pred == 0:
            return ['SPEED']
        if pred == 1:
            return ['RREAK']
        if pred == 3:
            return ['MOVE_LEFT']
        if pred == 4:
            return ['MOVE_RIGHT']
        if pred == 5:
            return ['SPEED', 'MOVE_LEFT']
        if pred == 6:
            return ['SPEED', 'MOVE_RIGHT']
        if pred == 7:
            return ['BREAK', 'MOVE_LEFT']
        if pred == 8:
            return ['BREAK', 'MOVE_RIGHT']
        else:
            return []


    def reset(self):
        """
        Reset the status
        """
        pass
