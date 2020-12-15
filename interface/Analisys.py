from pathlib import Path
import cv2
import math
import json
import os
import pandas as pd


def analysis(path=None):

    if path:
        json_yolo = os.path.join(path, "yolo.json")
        json_openpose = os.path.join(path, "openpose.json")
        video_path = os.path.join(path, "video-frames.mp4")
        trajektoria = os.path.join(path, "trajektoria.mp4")
        photo = os.path.join(path.replace("video", ""), "img/analysis")
        pozycja = os.path.join(path.replace(
            "video", ""), "img/analysis/pozycja_")
        jsonPath = os.path.join(path, "analiza.json")
    else:
        json_yolo = '..\\static\\interface\\video\\yolo.json'
        json_openpose = '..\\static\\interface\\video\\openpose.json'
        video_path = '..\\static\\interface\\video\\video-frames.mp4'
        trajektoria = '..\\static\\interface\\video\\trajektoria.mp4'
        photo = "..\\static\\interface\\img\\analysis"
        pozycja = "..\\static\\interface\\img\\analysis\\pozycja_"
        jsonPath = '..\\static\\interface\\video\\analiza.json'

    data = []

    with open(json_yolo) as json_file:  # otwarcie jsona dla YOLO
        data = json.load(json_file)

    with open(json_openpose) as json_file:  # otwarcie jsona OP
        data_op = json.load(json_file)

    df_rows = list()
    for frame_id, frame in enumerate(data):
        for obj in frame:
            df_rows.append([frame_id, obj['name'], obj['percentage_probability'],
                            *obj['box_points']])  # stworzenie Data Frame z YOLO

    df_yolo = pd.DataFrame(df_rows, columns=[
        "frame", "object", "proba", "x1", "y1", "x2", "y2"])  # nazwy kolumn

    all_frames = df_yolo["frame"].max()  # ilość wszystkich klatek
    # print(all_frames)
    all = df_yolo['object'].value_counts()
    # print(all) # drukuje wszystkie

    # stworzenie dataframe z rim, gdzie jest ponad 90 %
    rim = df_yolo[(df_yolo['object']) == 'rim']
    gproba_rim = rim[rim['proba'] > 90]
    # stworzenie dataframe z ball, gdzie jest ponad 60 %
    ball = df_yolo[(df_yolo['object']) == 'ball']
    gproba_ball = ball[ball['proba'] > 60]
    # stworzenie dataframe z people, gdzie jest ponad 80 %
    people = df_yolo[(df_yolo['object']) == 'people']
    gproba_pp = people[people['proba'] > 80]
    # połączenie trzech dataframe w jedno

    # połączenie 3 DF
    df_yolo = pd.concat([gproba_pp, gproba_ball, gproba_rim])
    df_yolo_all = df_yolo.copy()
    df_people_cords = df_yolo.copy()

    all_good = df_yolo['object'].value_counts()
    # print(all_good) # drukuje prawidłowe

    # df_yolo.head()

    # sprawdzanie ile klatek jest poprawnych (3 elementy)
    count_frames = df_yolo["frame"].max()  # wszystkie klatki
    n = 0
    is_good = 0  # zmienna przechwująca dobre klatki
    good_frames = []  # lista przechowująca dobre klatki

    while n < count_frames:
        one_frame = df_yolo[(df_yolo['frame']) == n]
        # zliczanie ile mamy obiektów w  danej klatce
        x = one_frame['object'].count()
        if "rim" in one_frame.values and "people" in one_frame.values and 'ball' in one_frame.values and x == 3:
            # print("Klatka",n,"jest dobra")
            is_good += 1
            good_frames.append(n)
        else:
            # print("Klatka",n,"nie jest dobra")
            df_yolo = df_yolo[df_yolo.frame != n]
        n += 1
    print("Dobrych klatek:", is_good)
    ratio = is_good/count_frames  # jaki współczynnik klatek jest dobry
    print("Wspolczynnik dobrych:", ratio)
    if ratio > 0.5:
        print("Film się nadaje ")
        film = True
    else:
        print("Film się nie nadaje")
        film = False
    # df_yolo.head()

    # Data Frame OP
    df_rows = list()
    for frame_id, frame in enumerate(data_op):
        for person_id, person in enumerate(frame['persons']):
            for part_id, part in enumerate(person):
                df_rows.append([frame_id, person_id, part_id, *part])

    df_op = pd.DataFrame(df_rows, columns=[
        "frame", "person", "part", "x", "y", "proba"])  # stworzenie DF dla OpenPose
    df_op_all = df_op.copy()

    # usuwanie niepotrzebych punktów
    # punkty na człowieku których nie używamy
    points = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
    for i in points:
        df_op = df_op[df_op.part != i]
    # print(df_op)

    # sprawdzenie wiekszego prawdopodobieństwa i usunięcie osób jeśli jest więcej niż jedna
    for frame_id, df_frame in df_op.groupby("frame"):
        probas = []
        for person_id, df_person in df_frame.groupby("person"):
            probas.append(df_person['proba'].mean())
        person_correct_id = probas.index(max(probas))
        df_op = df_op[(df_op["frame"] != frame_id) | (
            (df_op["frame"] == frame_id) & (df_op["person"] == person_correct_id))]
        df_op_all = df_op[(df_op["frame"] != frame_id) | (
            (df_op["frame"] == frame_id) & (df_op["person"] == person_correct_id))]
    # jaka osoba została na klatce
    # for frame_id, df_frame in df_op.groupby("frame"):
    #   print(df_frame["person"].unique())
    df_new = df_op.copy()
    # print(df_op)

    # sprawdzamy czy człowiek (YOLO) jest w człowieku (OP)
    one_frame_yolo = df_yolo[(df_yolo['frame'].isin(
        good_frames)) & (df_yolo['object'] == 'people')]
    one_frame_op = df_op[(df_op['frame'].isin(good_frames))
                         & (df_op['part'] == 8)]
    # merge obu dataframe
    person_check = pd.merge(one_frame_yolo, one_frame_op,
                            how='inner', on='frame')
    # sprawdzamy czy środek człowieka z OpenPose znajduje się wewnątrz ramki People z Yolo

    def person_condition(x1, x2, x, y1, y2, y):
        if x1 < x and x2 > x and y1 < y and y2 > y:
            return True
        return False

    person_check['good'] = [person_condition(*row) for row in zip(person_check['x1'], person_check['x2'],
                                                                  person_check['x'], person_check['y1'], person_check['y2'], person_check['y'])]
    person_ratio = person_check['good'].value_counts(
    ).loc[True] / person_check.shape[0]

    if person_ratio > 0.90 and film == True:
        # print("Dobry film", person_ratio)
        film = True
    else:
        # print("Zły film", person_ratio)
        film = False

    # Tworzenie nowego DF, który ma wsp. środka piłki i wybranych 4 punktów na człowieku
    yolo_ball_frames = []  # lista dobrych klatek
    for frame_id, df_frame in df_yolo_all.groupby("frame"):
        ball_counter = df_frame['object'].value_counts()
        if 'ball' in ball_counter.index and ball_counter.loc['ball'] == 1:
            yolo_ball_frames.append(frame_id)

    df_yolo_all = df_yolo_all[(df_yolo_all["object"] == 'ball') & (
        df_yolo_all['frame'].isin(yolo_ball_frames))]

    # środek piłki
    df_yolo_all['x_center'] = abs((df_yolo_all['x1'] + df_yolo_all['x2'])/2)
    df_yolo_all['y_center'] = abs((df_yolo_all['y1'] + df_yolo_all['y2'])/2)

    df_op_all = df_op_all[(df_op_all['frame'].isin(yolo_ball_frames)) & (
        df_op_all['part'].isin([1, 4, 7, 8]))]  # klatki

    dict_x_y = {}  # słownik częsci ciała

    def part_x_y(d, frame_id, part_id, p_x, p_y):  # d - słownik
        frame_key = 'frame_' + str(frame_id)  # klucz słownika
        part_key = '_part_' + str(part_id)  # nazwa części ciała - klucz
        if frame_key not in d.keys():
            # jeśli ramki nie ma to musi ją utworzyć w słowniku
            d[frame_key] = {'frame': frame_id}
        d[frame_key]['x' + part_key] = p_x  # współrzędna x
        d[frame_key]['y' + part_key] = p_y  # współrzędna y

    _ = [part_x_y(dict_x_y, *row) for row in zip(df_op_all['frame'],
                                                 df_op_all['part'], df_op_all['x'], df_op_all['y'])]  # wyrażenie listowe

    df_concat = pd.merge(df_yolo_all, pd.DataFrame(
        list(dict_x_y.values())), how='inner', on='frame')  # połączenie
    df_concat.drop(['object', 'proba', 'x1', 'y1', 'x2', 'y2'],
                   axis=1, inplace=True)  # usuniecie kolumn niepotrzebnych
    # df_concat.head()

    # Obliczanie odległości pomiędzy srodkiem piłki a wybranymi punktami na człowieku

    tab_1 = []
    tab_4 = []
    tab_7 = []
    tab_8 = []

    for n in yolo_ball_frames:
        one_frame = df_concat[(df_concat['frame']) == n]

    # wyciągamy koordynaty punktów i środka piłki
        x_1 = one_frame['x_part_1'].item()
        y_1 = one_frame['y_part_1'].item()
        x_center = one_frame['x_center'].item()
        y_center = one_frame['y_center'].item()

        x_4 = one_frame['x_part_4'].item()
        y_4 = one_frame['y_part_4'].item()

        x_7 = one_frame['x_part_7'].item()
        y_7 = one_frame['y_part_7'].item()

        x_8 = one_frame['x_part_8'].item()
        y_8 = one_frame['y_part_8'].item()

    # obliczamy odległość między środkiem piłki a punktami i dodanie do tablic

        tab_1.append(math.sqrt((x_center - x_1)**2 + (y_center - y_1)**2))
        tab_4.append(math.sqrt((x_center - x_4)**2 + (y_center - y_4)**2))
        tab_7.append(math.sqrt((x_center - x_7)**2 + (y_center - y_7)**2))
        tab_8.append(math.sqrt((x_center - x_8)**2 + (y_center - y_8)**2))

    # dodanie tablic jako kolumn

    df_concat['dist_1'] = tab_1  # Odległość punktu (1) od środka piłki
    df_concat['dist_4'] = tab_4  # Odległość punktu (4) od środka piłki
    df_concat['dist_7'] = tab_7  # Odległość punktu (7) od środka piłki
    df_concat['dist_8'] = tab_8  # Odległość punktu (8) od środka piłki

    pd.set_option('display.max_rows', None)  # pokazuje cały dataframe
    pd.set_option('display.max_columns', None)

    df_ball_cords = df_concat.copy()
    df_ball_cords.drop(['x_part_1', 'x_part_4', 'x_part_7', 'x_part_8', 'y_part_1', 'y_part_4',
                        'y_part_7', 'y_part_8', 'dist_1', 'dist_4', 'dist_7', 'dist_8'], axis=1, inplace=True)
    df_concat.drop(['x_center', 'y_center', 'x_part_1', 'x_part_4', 'x_part_7',
                    'x_part_8', 'y_part_1', 'y_part_4', 'y_part_7', 'y_part_8'], axis=1, inplace=True)
    # df_concat.head()

    # Obliczanie, która klatka to wybrana pozycja
    # 1 pozycja - piłka najbliżej punktu  8
    min_8 = df_concat['dist_8'].min()
    five_frames = []
    for n in yolo_ball_frames:
        one_frame = df_concat[(df_concat['frame']) == n]
        eight = one_frame['dist_8'].item()
        if eight == min_8:
            five_frames.append(n)

    # usunięcie wszystkich klatek przed 1 pozycją
    df_concat_clean = df_concat[df_concat['frame'] >= five_frames[0]]

    # 3 i 4 pozycja - piłka ostatni raz dotyka rąk (punkt 4 i 7) i pierwszy raz ich nie dotyka
    epsilon = 50
    df_concat_clean = df_concat_clean[['dist_4', 'dist_7']].diff().apply(
        abs)  # różnica między poprzednimi ramkami
    df_concat_clean['sub'] = (df_concat_clean['dist_4'] -
                              df_concat_clean['dist_7']).apply(abs)
    # usuwamy ramki w których różnica odległości rąk od środka piłki jest za duża (granica błędu)
    df_concat_clean = df_concat_clean[df_concat_clean['sub'] < 50]

    # srednia ruchoma da 5 klatek, jeśli jest za duża to rzut jest w tych klatkach
    df_clean_average = df_concat_clean.rolling(5, center=True).sum()
    df_clean_average = df_clean_average[(df_clean_average['dist_4'] >= 100) | (
        df_clean_average['dist_7'] >= 100)]
    pose_3 = df_concat.loc[df_clean_average.index[0] + 1, 'frame']
    pose_4 = df_concat.loc[df_clean_average.index[0] + 2, 'frame']

    five_frames.append(pose_3)  # 3 pozycja
    five_frames.append(pose_4)  # 4 pozycja

    # df_five_frames = df_new[df_new['frame'].isin(five_frames)] # dataset (OP) z ramek z 4 pozycji

    df_concat_2 = df_concat[df_concat['frame'] != pose_3]
    df_concat_2 = df_concat_2[df_concat_2['frame'] != pose_4]

    yolo_ball_frames = [
        item for item in yolo_ball_frames if item not in five_frames]

    # 2 pozycja - piłka najbliżej punktu  1

    min_1 = df_concat_2['dist_1'].min()
    for n in yolo_ball_frames:
        one_frame = df_concat_2[(df_concat_2['frame']) == n]
        one = one_frame['dist_1'].item()
        if one == min_1:
            five_frames.append(n)

    # 5 klatka - koniec rzutu (trafiony lub nie)

    dis_frames = []
    # dis_frames = [] # numer ramki, odległość srodka pilki od srodka ramki
    x = 0  # zmienna przechowująca ramke, w ktorej konczy się rzut

    for n in good_frames:
        one_frame = df_yolo[(df_yolo['frame']) == n]
    # wyciągamy koordynaty piłki
        ball_cords = one_frame[(one_frame['object']) == 'ball']
        b_x1 = ball_cords['x1'].item()
        b_x2 = ball_cords['x2'].item()
        b_y1 = ball_cords['y1'].item()
        b_y2 = ball_cords['y2'].item()
    # wyliczamy środek piłki
        b_x = (b_x1 + b_x2)/2
        b_y = (b_y1 + b_y2)/2
    # wyciągamy koordynaty ramki
        rim_cords = one_frame[(one_frame['object']) == 'rim']
        r_x1 = rim_cords['x1'].item()
        r_x2 = rim_cords['x2'].item()
        r_y1 = rim_cords['y1'].item()
        r_y2 = rim_cords['y2'].item()
    # wyliczamy środek obręczy
        r_x = (r_x1 + r_x2)/2
        r_y = (r_y1 + r_y2)/2
    # obliczamy odległość między środkiem piłki a punktami
        d_1 = math.sqrt((b_x - r_x)**2 + (b_y - r_y)**2)
        d_1 = abs(d_1)

        # tablica przechowująca odległości i numer klatki
        dis_frames.append([d_1, n])

    mini_dist = min(dis_frames)
    # numer klatki z najmniejszą odległością piłki od obręczy
    mini_dist_frame = mini_dist[1]
    five_frames.append(mini_dist_frame)  # dodanie piątej klatki
    # print(five_frames)

    # Sprawdzenie skuteczności rzutu na klatce pozycji 5
    one_frame = df_yolo[(df_yolo['frame']) == mini_dist_frame]
    # wyciągamy koordynaty piłki
    ball_cords = one_frame[(one_frame['object']) == 'ball']
    b_x1 = ball_cords['x1'].item()
    b_x2 = ball_cords['x2'].item()
    b_y1 = ball_cords['y1'].item()
    b_y2 = ball_cords['y2'].item()
    # wyliczamy środek piłki
    b_x = (b_x1 + b_x2)/2
    b_y = (b_y1 + b_y2)/2
    # wyciągamy koordynaty ramki
    rim_cords = one_frame[(one_frame['object']) == 'rim']
    r_x1 = rim_cords['x1'].item()
    r_x2 = rim_cords['x2'].item()
    r_y1 = rim_cords['y1'].item()
    r_y2 = rim_cords['y2'].item()

    # sprawdzamy czy środek piłki przeszedł przez ramkę
    if r_x1 < b_x and r_x2 > b_x and r_y1 < b_y and r_y2 > b_y:
        #print(mini_dist_frame, "TRAFIONE!")
        throw = True
    else:
        throw = False

    # Rysowanie trajektori lotu piłki

    # print(df_ball_cords) # nowy df ze środkiem piłki na każdej klatce
    index_1 = good_frames.index(five_frames[3])
    index_2 = good_frames.index(five_frames[4]) - 1
    ball_frames = good_frames[index_1:min(index_2, len(good_frames) - 1)]
    frame_counter = 0
    distance = []
    # Create a VideoCapture object
    cap = cv2.VideoCapture(video_path)

    # Default resolutions of the frame are obtained.The default resolutions are system dependent.
    # We convert the resolutions from float to integer.
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
    out = cv2.VideoWriter(trajektoria, cv2.VideoWriter_fourcc(
        *'H264'), 30, (frame_width, frame_height))

    lines = []
    while(True):
        ret, frame = cap.read()

        if ret == True:
            if frame_counter in ball_frames:
                frame_index = df_ball_cords[df_ball_cords["frame"]
                                            == frame_counter].index[0] - 1
                # describe the type of font to be used.
                font = cv2.FONT_HERSHEY_SIMPLEX
                start_x = int(df_ball_cords.loc[frame_index, "x_center"])
                end_x = int(df_ball_cords.loc[min(
                    frame_index + 1, df_ball_cords.shape[0] - 1), "x_center"])
                lines.append({
                    "start": (
                        start_x,
                        int(df_ball_cords.loc[frame_index, "y_center"])
                    ),
                    "end": (
                        end_x,
                        int(df_ball_cords.loc[min(
                            frame_index + 1, df_ball_cords.shape[0] - 1), "y_center"])
                    )
                })

                substract = abs(end_x - start_x)
                distance.append(substract)

            for line in lines:
                # Use putText() method for inserting text on video
                cv2.line(
                    frame,
                    line["start"],
                    line["end"],
                    (255, 255, 255),
                    5
                )

            # Write the frame into the file 'output.avi'
            out.write(frame)
            # Increase frame counter
            frame_counter += 1

        # Break the loop
        else:
            break

    # Zapisywanie wybranych klatek do jpg
    for frm in five_frames:
        cap.set(1, frm)
        ret, frame = cap.read()
        cv2.imwrite(photo +
                    str(frm)+".jpg", frame)

    # Crop wybranych klatek zapisywanych wyżej
    people_c = df_people_cords[df_people_cords['frame'] == five_frames[2]]
    people_cords = people_c[(people_c['object']) == 'people']
    p_x1 = people_cords['x1'].item()
    p_y1 = people_cords['y1'].item()
    p_x2 = people_cords['x2'].item()
    p_y2 = people_cords['y2'].item()
    n = 1

    for i in five_frames[:-1]:
        img = cv2.imread(photo + str(i)+".jpg")
        crop_img = img[p_y1 - 50:p_y2 + 100, p_x1 - 50:p_x2 + 100]
        cv2.imwrite(pozycja +
                    str(n)+".jpg", crop_img)
        n += 1

    # When everything done, release the video capture and video write objects
    cap.release()
    out.release()

    # Closes all the frames
    cv2.destroyAllWindows()

    # INFO OUTPUTOWE
    # WYBRANE KLATKI
    five_frames.sort()
    print("Wybrane 5 klatek to ", five_frames)

    # CZY FILM SIĘ NADAJE
    to_json = {}
    if film == True:

        print("Film się nadaje")
        # CZAS
        # Ile minęło od pozycji pierszej do czwartej (od przygotowania do rzutu)
        counter_start = five_frames[3]-five_frames[0]  # ile klatek
        counter_start = round((counter_start/30), 2)  # sekundy
        print("Przygotowanie do rzutu trwa", counter_start, "s")
        to_json.update(
            {"Przygotowanie do rzutu trwa": str(counter_start) + "s"})

        # Ile minęło od pozycji czwartej do piątek (rzut)
        counter_throw = five_frames[4]-five_frames[3]  # ile klatek
        counter_throw = round((counter_throw/30), 2)   # sekundy
        print("Rzut trwa", counter_throw, "s")
        to_json.update({"Rzut trwa": str(counter_throw) + "s"})

        # Skuteczność rzutu
        if throw == True:
            print("Rzut trafiony")
            to_json.update({"Rzut trafiony": "tak"})
        else:
            print("Rzut nie trafiony")
            to_json.update({"Rzut trafiony": "nie"})
        df_new

        # Obliczanie prędkości piłki
        df_pos_3 = df_new[df_new['frame'] == five_frames[2]]
        foot = df_pos_3[df_pos_3['part'] == 11]
        foot_x = foot['x'].item()  # współrzędna x stopy
        rim_cords = one_frame[(one_frame['object']) == 'rim']
        r_x1 = rim_cords['x1'].item()
        r_x2 = rim_cords['x2'].item()
        rim_x = (r_x1 + r_x2)/2  # współrzędna x środka rimu
        # odleglość stopy od rimu w pikselach
        dist_rim_ft = round(abs(rim_x-foot_x))
        sum_distance = sum(distance)  # droga piłki w pikselach
        wsp = 400/dist_rim_ft
        path = (sum_distance*wsp)/100  # przeliczenie lotu pilki na cm
        speed = round(path / counter_throw, 2)
        print("Prędkość piłki to", speed, 'm/s')
        to_json.update({"Prędkość piłki to": str(speed) + "m/s"})

        # Wyskok
        df_pos = df_new[df_new['frame'] == five_frames[0]]
        foot = df_pos[df_pos['part'] == 11]
        foot_y_1 = foot['y'].item()  # współrzędna y stopy w 1 wybranej pozycji
        df_pos = df_new[df_new['frame'] == five_frames[3]]
        foot = df_pos[df_pos['part'] == 11]
        foot_y_4 = foot['y'].item()  # współrzędna y stopy w 4 wybranej pozycji
        hop = round(abs(foot_y_4 - foot_y_1), 2)  # wyskok w pikselach
        hop_cm = round(hop*wsp, 2)  # wyskok w cm
        if (hop_cm > 5):
            print("Wysokość wyskoku wynosi", hop_cm, "cm")
            to_json.update({"Wysokość wyskoku wynosi": str(hop_cm) + "cm"})

        # Kąt łokcia rzut prawą ręką
        df_pos_elbow = df_new[df_new['frame'] == five_frames[2]]
        df_pos_elbow_2 = df_pos_elbow[df_pos_elbow['part'] == 2]
        elbow_x_2 = df_pos_elbow_2['x'].item()
        elbow_y_2 = df_pos_elbow_2['y'].item()
        df_pos_elbow_3 = df_pos_elbow[df_pos_elbow['part'] == 3]
        elbow_x_3 = df_pos_elbow_3['x'].item()
        elbow_y_3 = df_pos_elbow_3['y'].item()
        df_pos_elbow_4 = df_pos_elbow[df_pos_elbow['part'] == 4]
        elbow_x_4 = df_pos_elbow_4['x'].item()
        elbow_y_4 = df_pos_elbow_4['y'].item()
        # obliczanie dlugosci ramion trojkata
        a = (math.sqrt((elbow_x_3 - elbow_x_2)**2 + (elbow_y_3 - elbow_y_2)**2))
        b = (math.sqrt((elbow_x_4 - elbow_x_3)**2 + (elbow_y_4 - elbow_y_3)**2))
        c = (math.sqrt((elbow_x_4 - elbow_x_2)**2 + (elbow_y_4 - elbow_y_2)**2))
        cosin_y = abs((a**2 + b**2 - c**2)/(2*a*b))  # Twierdzenie Cosinusów
        angle_right = round(math.degrees(math.acos(cosin_y)), 1)

        # Kąt łokcia rzut lewą ręką
        df_pos_elbow = df_new[df_new['frame'] == five_frames[2]]
        df_pos_elbow_5 = df_pos_elbow[df_pos_elbow['part'] == 5]
        elbow_x_5 = df_pos_elbow_5['x'].item()
        elbow_y_5 = df_pos_elbow_5['y'].item()
        df_pos_elbow_6 = df_pos_elbow[df_pos_elbow['part'] == 6]
        elbow_x_6 = df_pos_elbow_6['x'].item()
        elbow_y_6 = df_pos_elbow_6['y'].item()
        df_pos_elbow_7 = df_pos_elbow[df_pos_elbow['part'] == 7]
        elbow_x_7 = df_pos_elbow_7['x'].item()
        elbow_y_7 = df_pos_elbow_7['y'].item()
        # obliczanie dlugosci ramion trojkata
        a = (math.sqrt((elbow_x_6 - elbow_x_5)**2 + (elbow_y_6 - elbow_y_5)**2))
        b = (math.sqrt((elbow_x_7 - elbow_x_6)**2 + (elbow_y_7 - elbow_y_6)**2))
        c = (math.sqrt((elbow_x_7 - elbow_x_5)**2 + (elbow_y_7 - elbow_y_5)**2))
        cosin_y = abs((a**2 + b**2 - c**2)/(2*a*b))  # Twierdzenie Cosinusów
        angle_left = round(math.degrees(math.acos(cosin_y)), 1)

        if angle_right >= angle_left:
            print("Kąt łokcia w pozycji 3 to", angle_right, "stopni")
            to_json.update(
                {"Kąt łokcia w pozycji 3 to": str(angle_right) + " stopni"})
        else:
            print("Kąt łokcia w pozycji 3 to", angle_left, "stopni")
            to_json.update(
                {"Kąt łokcia w pozycji 3 to": str(angle_left) + " stopni"})
    else:
        print("Film się nie nadaje")
        to_json.update(
            {"Film się nie nadaje": "Oj nie byczq"})

    with open(jsonPath, 'w+') as f:
        f.write(json.dumps(to_json))
    return to_json


if __name__ == "__main__":
    analysis()
