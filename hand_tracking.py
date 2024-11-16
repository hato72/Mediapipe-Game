import cv2 as cv
#import numpy as np
import mediapipe as mp

from env import *

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    model_complexity=1,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5,
)


class Hand_tracking:
    def __init__(self):
        self.hands = hands
        self.hand_x = 0
        self.hand_y = 0
        self.results = None
        self.hand_close = False

    def hand_tracking(self,image):
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        image.flags.writeable = False
        self.results = self.hands.process(image)

        image.flags.writeable = True
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
        #print("hand tracking")

        self.hand_close = False

        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                joint_x,joint_y = hand_landmarks.landmark[9].x, hand_landmarks.landmark[9].y

                self.hand_x = int(joint_x * screen_width)
                self.hand_y = int(joint_y * screen_height)

                _,tip_y = hand_landmarks.landmark[12].x, hand_landmarks.landmark[12].y

                if tip_y > joint_y:
                    self.hand_close = True

                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

        return image
    
    
    def get_hand_center(self):
        return (self.hand_x, self.hand_y)
    
    def display_hand(self):
        cv.imshow("image",self.image)
        cv.waitKey(1)
        # if key == 27:  # ESC
        #     pass


# def main():

#     # World座標プロット 
#     if plot_world_landmark:
#         import matplotlib.pyplot as plt

#         fig = plt.figure()
#         r_ax = fig.add_subplot(121, projection="3d")
#         l_ax = fig.add_subplot(122, projection="3d")
#         fig.subplots_adjust(left=0.0, right=1, bottom=0, top=1)
        
#     with hands:
#         while cap.isOpened():
#             ret, image = cap.read()
#             if not ret:
#                 break
#             image = cv.flip(image, 1)  # ミラー表示
#             debug_image = copy.deepcopy(image)

#             image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
#             results = hands.process(image)

#             # 描画
#             if results.multi_hand_landmarks is not None:
#                 for hand_landmarks, handedness in zip(results.multi_hand_landmarks,
#                                                     results.multi_handedness):
#                     # 手の平重心計算
#                     cx, cy = calc_palm_moment(debug_image, hand_landmarks)
#                     # 外接矩形の計算
#                     brect = calc_bounding_rect(debug_image, hand_landmarks)
#                     # 描画
#                     debug_image = draw_landmarks(debug_image, cx, cy,
#                                                 hand_landmarks, handedness)
#                     debug_image = draw_bounding_rect(use_brect, debug_image, brect)

#             # cv.putText(debug_image, "FPS:" + str(display_fps), (10, 30),
#             #            cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2, cv.LINE_AA)

#             # World座標プロット
#             if plot_world_landmark:
#                 if results.multi_hand_world_landmarks is not None:
#                     plot_world_landmarks(
#                         plt,
#                         [r_ax, l_ax],
#                         results.multi_hand_world_landmarks,
#                         results.multi_handedness,
#                     )

#             # キー処理(ESC：終了) 
#             key = cv.waitKey(1)
#             if key == 27:  # ESC
#                 break

#             # 画面反映 
#             cv.imshow('MediaPipe Hand Demo', debug_image)

#         cap.release()
#     cv.destroyAllWindows()


# def calc_palm_moment(image, landmarks):
#     image_width, image_height = image.shape[1], image.shape[0]

#     palm_array = np.empty((0, 2), int)

#     for index, landmark in enumerate(landmarks.landmark):
#         landmark_x = min(int(landmark.x * image_width), image_width - 1)
#         landmark_y = min(int(landmark.y * image_height), image_height - 1)

#         landmark_point = [np.array((landmark_x, landmark_y))]

#         if index == 0:  # 手首1
#             palm_array = np.append(palm_array, landmark_point, axis=0)
#         if index == 1:  # 手首2
#             palm_array = np.append(palm_array, landmark_point, axis=0)
#         if index == 5:  # 人差指：付け根
#             palm_array = np.append(palm_array, landmark_point, axis=0)
#         if index == 9:  # 中指：付け根
#             palm_array = np.append(palm_array, landmark_point, axis=0)
#         if index == 13:  # 薬指：付け根
#             palm_array = np.append(palm_array, landmark_point, axis=0)
#         if index == 17:  # 小指：付け根
#             palm_array = np.append(palm_array, landmark_point, axis=0)
#     M = cv.moments(palm_array)
#     cx, cy = 0, 0
#     if M['m00'] != 0:
#         cx = int(M['m10'] / M['m00'])
#         cy = int(M['m01'] / M['m00'])

#     return cx, cy


# def calc_bounding_rect(image, landmarks):
#     image_width, image_height = image.shape[1], image.shape[0]

#     landmark_array = np.empty((0, 2), int)

#     for _, landmark in enumerate(landmarks.landmark):
#         landmark_x = min(int(landmark.x * image_width), image_width - 1)
#         landmark_y = min(int(landmark.y * image_height), image_height - 1)

#         landmark_point = [np.array((landmark_x, landmark_y))]

#         landmark_array = np.append(landmark_array, landmark_point, axis=0)

#     x, y, w, h = cv.boundingRect(landmark_array)

#     return [x, y, x + w, y + h]


# def draw_landmarks(image, cx, cy, landmarks, handedness):
#     image_width, image_height = image.shape[1], image.shape[0]

#     landmark_point = []

#     # キーポイント
#     for index, landmark in enumerate(landmarks.landmark):
#         if landmark.visibility < 0 or landmark.presence < 0:
#             retry

#         landmark_x = min(int(landmark.x * image_width), image_width - 1)
#         landmark_y = min(int(landmark.y * image_height), image_height - 1)
#         # landmark_z = landmark.z

#         landmark_point.append((landmark_x, landmark_y))

#         if index == 0:  # 手首1
#             cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
#         if index == 1:  # 手首2
#             cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
#         if index == 2:  # 親指：付け根
#             cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
#         if index == 3:  # 親指：第1関節
#             cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
#         if index == 4:  # 親指：指先
#             cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
#             cv.circle(image, (landmark_x, landmark_y), 12, (0, 255, 0), 2)
#         if index == 5:  # 人差指：付け根
#             cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
#         if index == 6:  # 人差指：第2関節
#             cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
#         if index == 7:  # 人差指：第1関節
#             cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
#         if index == 8:  # 人差指：指先
#             cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
#             cv.circle(image, (landmark_x, landmark_y), 12, (0, 255, 0), 2)
#         if index == 9:  # 中指：付け根
#             cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
#         if index == 10:  # 中指：第2関節
#             cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
#         if index == 11:  # 中指：第1関節
#             cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
#         if index == 12:  # 中指：指先
#             cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
#             cv.circle(image, (landmark_x, landmark_y), 12, (0, 255, 0), 2)
#         if index == 13:  # 薬指：付け根
#             cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
#         if index == 14:  # 薬指：第2関節
#             cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
#         if index == 15:  # 薬指：第1関節
#             cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
#         if index == 16:  # 薬指：指先
#             cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
#             cv.circle(image, (landmark_x, landmark_y), 12, (0, 255, 0), 2)
#         if index == 17:  # 小指：付け根
#             cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
#         if index == 18:  # 小指：第2関節
#             cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
#         if index == 19:  # 小指：第1関節
#             cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
#         if index == 20:  # 小指：指先
#             cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
#             cv.circle(image, (landmark_x, landmark_y), 12, (0, 255, 0), 2)

#     # 接続線
#     if len(landmark_point) > 0:
#         # 親指
#         cv.line(image, landmark_point[2], landmark_point[3], (0, 255, 0), 2)
#         cv.line(image, landmark_point[3], landmark_point[4], (0, 255, 0), 2)

#         # 人差指
#         cv.line(image, landmark_point[5], landmark_point[6], (0, 255, 0), 2)
#         cv.line(image, landmark_point[6], landmark_point[7], (0, 255, 0), 2)
#         cv.line(image, landmark_point[7], landmark_point[8], (0, 255, 0), 2)

#         # 中指
#         cv.line(image, landmark_point[9], landmark_point[10], (0, 255, 0), 2)
#         cv.line(image, landmark_point[10], landmark_point[11], (0, 255, 0), 2)
#         cv.line(image, landmark_point[11], landmark_point[12], (0, 255, 0), 2)

#         # 薬指
#         cv.line(image, landmark_point[13], landmark_point[14], (0, 255, 0), 2)
#         cv.line(image, landmark_point[14], landmark_point[15], (0, 255, 0), 2)
#         cv.line(image, landmark_point[15], landmark_point[16], (0, 255, 0), 2)

#         # 小指
#         cv.line(image, landmark_point[17], landmark_point[18], (0, 255, 0), 2)
#         cv.line(image, landmark_point[18], landmark_point[19], (0, 255, 0), 2)
#         cv.line(image, landmark_point[19], landmark_point[20], (0, 255, 0), 2)

#         # 手の平
#         cv.line(image, landmark_point[0], landmark_point[1], (0, 255, 0), 2)
#         cv.line(image, landmark_point[1], landmark_point[2], (0, 255, 0), 2)
#         cv.line(image, landmark_point[2], landmark_point[5], (0, 255, 0), 2)
#         cv.line(image, landmark_point[5], landmark_point[9], (0, 255, 0), 2)
#         cv.line(image, landmark_point[9], landmark_point[13], (0, 255, 0), 2)
#         cv.line(image, landmark_point[13], landmark_point[17], (0, 255, 0), 2)
#         cv.line(image, landmark_point[17], landmark_point[0], (0, 255, 0), 2)

#     # 重心 + 左右
#     if len(landmark_point) > 0:
#         # handedness.classification[0].index
#         # handedness.classification[0].score

#         cv.circle(image, (cx, cy), 12, (0, 255, 0), 2)
#         cv.putText(image, handedness.classification[0].label[0],
#                    (cx - 6, cy + 6), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0),
#                    2, cv.LINE_AA)  # label[0]:一文字目だけ

#     return image


# def plot_world_landmarks(
#     plt,
#     ax_list,
#     multi_hands_landmarks,
#     multi_handedness,
#     visibility_th=0.5,
# ):
#     ax_list[0].cla()
#     ax_list[0].set_xlim3d(-0.1, 0.1)
#     ax_list[0].set_ylim3d(-0.1, 0.1)
#     ax_list[0].set_zlim3d(-0.1, 0.1)
#     ax_list[1].cla()
#     ax_list[1].set_xlim3d(-0.1, 0.1)
#     ax_list[1].set_ylim3d(-0.1, 0.1)
#     ax_list[1].set_zlim3d(-0.1, 0.1)

#     for landmarks, handedness in zip(multi_hands_landmarks, multi_handedness):
#         handedness_index = 0
#         if handedness.classification[0].label == 'Left':
#             handedness_index = 0
#         elif handedness.classification[0].label == 'Right':
#             handedness_index = 1

#         landmark_point = []

#         for index, landmark in enumerate(landmarks.landmark):
#             landmark_point.append(
#                 [landmark.visibility, (landmark.x, landmark.y, landmark.z)])

#         palm_list = [0, 1, 5, 9, 13, 17, 0]
#         thumb_list = [1, 2, 3, 4]
#         index_finger_list = [5, 6, 7, 8]
#         middle_finger_list = [9, 10, 11, 12]
#         ring_finger_list = [13, 14, 15, 16]
#         pinky_list = [17, 18, 19, 20]

#         # 掌
#         palm_x, palm_y, palm_z = [], [], []
#         for index in palm_list:
#             point = landmark_point[index][1]
#             palm_x.append(point[0])
#             palm_y.append(point[2])
#             palm_z.append(point[1] * (-1))

#         # 親指
#         thumb_x, thumb_y, thumb_z = [], [], []
#         for index in thumb_list:
#             point = landmark_point[index][1]
#             thumb_x.append(point[0])
#             thumb_y.append(point[2])
#             thumb_z.append(point[1] * (-1))

#         # 人差し指
#         index_finger_x, index_finger_y, index_finger_z = [], [], []
#         for index in index_finger_list:
#             point = landmark_point[index][1]
#             index_finger_x.append(point[0])
#             index_finger_y.append(point[2])
#             index_finger_z.append(point[1] * (-1))

#         # 中指
#         middle_finger_x, middle_finger_y, middle_finger_z = [], [], []
#         for index in middle_finger_list:
#             point = landmark_point[index][1]
#             middle_finger_x.append(point[0])
#             middle_finger_y.append(point[2])
#             middle_finger_z.append(point[1] * (-1))

#         # 薬指
#         ring_finger_x, ring_finger_y, ring_finger_z = [], [], []
#         for index in ring_finger_list:
#             point = landmark_point[index][1]
#             ring_finger_x.append(point[0])
#             ring_finger_y.append(point[2])
#             ring_finger_z.append(point[1] * (-1))

#         # 小指
#         pinky_x, pinky_y, pinky_z = [], [], []
#         for index in pinky_list:
#             point = landmark_point[index][1]
#             pinky_x.append(point[0])
#             pinky_y.append(point[2])
#             pinky_z.append(point[1] * (-1))

#         ax_list[handedness_index].plot(palm_x, palm_y, palm_z)
#         ax_list[handedness_index].plot(thumb_x, thumb_y, thumb_z)
#         ax_list[handedness_index].plot(index_finger_x, index_finger_y,
#                                        index_finger_z)
#         ax_list[handedness_index].plot(middle_finger_x, middle_finger_y,
#                                        middle_finger_z)
#         ax_list[handedness_index].plot(ring_finger_x, ring_finger_y,
#                                        ring_finger_z)
#         ax_list[handedness_index].plot(pinky_x, pinky_y, pinky_z)

#     plt.pause(.001)

#     return


# def draw_bounding_rect(use_brect, image, brect):
#     if use_brect:
#         # 外接矩形
#         cv.rectangle(image, (brect[0], brect[1]), (brect[2], brect[3]),
#                      (0, 255, 0), 2)

#     return image


# if __name__ == '__main__':
#     main()