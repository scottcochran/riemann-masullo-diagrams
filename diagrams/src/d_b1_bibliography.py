"""B1: the works the manuscript's bibliography lists, and where its text cites each one.

Read from riemann-masullo's transcription of the manuscript at the pin (diagrams/src/paper.py), under rules 9 and
10 (PLAN.md). One row per bibliography entry, in the order printed: its key, the entry as the transcription prints
it (authors, title, venue, year), a link to the work from diagrams/src/papers.toml, and the pages of the text that
cite it, each opening the chapter card whose `Paper:` pages cover it. A citation is the paper's: the Lean cites none
of these works, and nothing here says it rests on one.

What it records, compared both ways:

- REFERENCES: every entry's id, in the order printed: its key, or `<key> (2)` for the second entry under a key;
- CITED: key -> transcription file -> the pages that cite it;
- UNCITED: the keys that no bracketed citation in the text names;
- SP_TAGS: the Stacks project's tags its citations name (`[SP, Tag 000B]`) -> the pages citing each. A tag of a
  tag's form (four characters, digits and capital letters) opens its page on the Stacks project; any other is drawn
  without a link, as not a tag.

The papers file must give every entry exactly one id, and name no other.
"""
import collections
import pathlib
import re
import tomllib

import chapter as CH
import draw
import items as I
import lib
import paper
import rm

ID = "B1"
SLUG = "bibliography"

# every entry of the bibliography, in the order printed: its key, or `<key> (2)` for a second entry under one
REFERENCES = ['AB', 'ABM', 'ABR', 'Ac', 'Ahl', 'Al-B', 'Apiola', 'Ara', 'Arm', 'Art-1', 'Art-2', 'Arthur', 'AS', 'AT', 'AtChe',
 'Au', 'Aub', 'Ba', 'Ba1', 'Ba2', 'Bar', 'BB', 'BCR', 'BCZ', 'Be', 'BG', 'BGV', 'Birkhoff', 'BJ', 'BJL', 'BJM',
 'BKMcK', 'Bl', 'BL', 'Bo', 'Bog', 'Bohr', 'Bohr1', 'Bohr2', 'Bohr3', 'Bohr4', 'Bor1', 'Bor2', 'Bou', 'Bou-I',
 'Bou-II', 'Bou-GT', 'Bou-TVS', 'Br1', 'Br2', 'Br3', 'Br4', 'Bris-a', 'Bris-b', 'Bru', 'BT', 'Car', 'Carleson',
 'CdSW', 'CF', 'CFSS', 'Ch', 'Cha', 'CHR', 'Cl', 'Cnw-a', 'Cnw-b', 'Cnw-c', 'Co', 'Coh', 'Conrad', 'CPS',
 'Davenport-1', 'Davenport-2', 'DE', 'Del', 'De', 'De2', 'De3', 'De4', 'Den', 'DiM', 'Dix', 'DS', 'DU', 'Du',
 'Dunford', 'Dur', 'DyM', 'E', 'EGAI', 'EGAII', 'EGAIII$_1$', 'EGAIII$_2$', 'EGAIV$_1$', 'EGAIV$_2$', 'EGAIV$_3$',
 'EGAIV$_4$', 'Ehr1', 'Ehr2', 'EK', 'ELS', 'EU', 'FG', 'FGT', 'FK', 'FlM', 'Flo', 'FM', 'Fol', 'Fol-2', 'For', 'Fr',
 'FSt', 'FujKa', 'Ga', 'Ga-1', 'Ga-2', 'Gao', 'Gdm', 'GE', 'GL', 'Gle', 'GNar', 'GoKre', 'Goss', 'GR', 'GRa', 'GrM',
 'Gro-a', 'Gro-b', 'Gro-c', 'Gro-d', 'Gro-e', 'Gro-f', 'GS', 'Ha', 'H', 'Hig', 'HK', 'HKZ', 'HL', 'HN', 'Horm', 'Hor',
 'HP', 'HR-1', 'HR-2', 'HS', 'HSS', 'HSt', 'Hu1', 'Hu2', 'Hunt', 'HuWe', 'HW', 'IK', 'Ingh1', 'Ingh2', 'Ingh3', 'Iw',
 'Iwaniec', 'Jar', 'Jech', 'JL', 'JL (2)', 'Jor-a', 'Jor-b', 'JPP', 'Ka', 'Kakutani', 'Kal', 'Katzn', 'Katzn (2)',
 'Kech', 'Ke-a', 'Ke-b', 'Ke', 'Kel', 'KG', 'Klee', 'KleMo', 'Kn', 'Kob', 'Kol', 'TKYK', 'Kothe-I', 'Kothe-II',
 'Kruse', 'KS', 'Kubota', 'Kub', 'Kudla', 'Kunen', 'La', 'Langlands', 'Lang-a', 'Lang-b', 'Lang-c', 'Lang-d',
 'Lang-e', 'Lang-f', 'LR', 'Lee', 'Les', 'LGL', 'Lit-I', 'Lit-II', 'LM', 'LMS', 'LT', 'M', 'MacL', 'MacL2', 'Mar',
 'May', 'Mat-I', 'Mat-II', 'McAr', 'McC', 'Me', 'Me1', 'Me2', 'Me3', 'Meg', 'Mi', 'Mit', 'MLei', 'Moroz', 'Mos', 'MS',
 'Mu', 'Murty', 'MV', 'MV-2', 'MVa', 'MVe', 'MZ', 'N', 'NB', 'Ng', 'Neu', 'Nik', 'nLab1', 'Oes', 'Omar', 'Pa', 'PB',
 'Pinsky', 'Quer', 'QQ', 'Ret', 'Rezk', 'Riemann', 'Ro', 'RS', 'Ryan', 'Ru-Sa', 'Ru', 'Ru-2', 'Ru-3', 'Rud-Sa', 'RV',
 'Sarnak', 'Sch-a', 'Sch-b', 'Scha', 'Schm', 'Series', 'Se', 'SGA1', 'SGA3', 'SGA4', 'Shi', 'Silverman', 'Simon',
 'Sm', 'SN', 'SO', 'SP', 'Struble', 'StSha-III', 'StSe', 'StStr', 'Ste', 'Str', 'SW', 'T1', 'T2', 'Tate', 'Tre',
 'TsV', 'Val-a', 'Val-b', 'VLH', 'VK', 'Vogt-1', 'Vogt-2', 'Voigt', 'Vogt', 'vO', 'Vor', 'Wa', 'Weil-a', 'Weil-b',
 'Weil-c', 'Weil-d', 'Weil-e', 'Weil-f', 'W', 'Wi', 'Wil', 'Wngr-1', 'Wngr-2', 'Wrn', 'Yos', 'Yos-2', 'Zagier', 'Za']
# key -> transcription file -> the pages that cite it
CITED = {'CF': {'front-matter.md': [7],
        'chapter-01.md': [33, 43],
        'chapter-02.md': [57, 74, 81, 82, 110, 113],
        'chapter-03.md': [117, 119, 120, 121, 122, 124, 126, 129, 130, 131, 132, 133, 134, 136, 137, 139, 141, 142,
                          144, 148],
        'chapter-05.md': [228, 256, 258, 273],
        'chapter-06.md': [298],
        'chapter-07.md': [316, 317, 332, 333, 336, 343, 365, 378, 379],
        'chapter-08.md': [386],
        'chapter-09.md': [403],
        'chapter-11.md': [484],
        'appendix-a.md': [537, 539, 541, 556, 557, 558, 559, 560, 561],
        'appendix-b.md': [636, 640],
        'appendix-d.md': [794]},
 'MS': {'chapter-01.md': [34]},
 'GS': {'chapter-01.md': [34]},
 'Me1': {'chapter-01.md': [39, 42], 'chapter-05.md': [222, 238], 'appendix-c.md': [693, 695]},
 'Co': {'chapter-01.md': [44],
        'chapter-02.md': [82, 100, 107, 110],
        'chapter-07.md': [326],
        'chapter-09.md': [396, 422],
        'chapter-10.md': [439, 447],
        'appendix-a.md': [561],
        'appendix-b.md': [617, 619, 621, 623]},
 'Jar': {'chapter-02.md': [59, 61, 62, 69, 70, 71, 84, 85, 103, 111],
         'chapter-04.md': [156, 157, 158, 159, 160, 161, 162, 164, 168, 169, 183, 195, 196, 197, 202, 205, 206, 207],
         'chapter-05.md': [226, 227, 229, 235, 242, 243, 244, 248, 253, 254, 255, 256, 260, 261, 262, 273, 281, 282,
                           283, 285],
         'chapter-06.md': [290, 299],
         'chapter-07.md': [311, 312, 330, 332, 342, 344, 349, 350, 353, 366, 371, 372, 376],
         'chapter-09.md': [431],
         'chapter-10.md': [438, 440, 451, 462, 463, 466, 469],
         'chapter-11.md': [484],
         'appendix-c.md': [657, 658, 663, 674, 677, 678, 679, 680, 686, 703, 704, 706],
         'appendix-d.md': [778, 809, 810]},
 'Sch-a': {'chapter-02.md': [59, 62],
           'chapter-04.md': [170, 194, 205],
           'chapter-05.md': [250, 251, 270],
           'chapter-07.md': [353]},
 'Scha': {'chapter-02.md': [59, 61, 68, 69, 70, 71, 72, 74, 84, 85, 88, 92, 114],
          'chapter-03.md': [125],
          'chapter-04.md': [161, 164, 165, 168, 169, 170, 176, 177, 202, 204, 205, 210, 220],
          'chapter-05.md': [223, 228, 229, 231, 235, 236, 237, 241, 243, 244, 248, 250, 253, 255, 267, 268, 285],
          'chapter-06.md': [289, 295],
          'chapter-07.md': [327, 331, 344, 370, 375],
          'chapter-09.md': [422, 429],
          'appendix-b.md': [626],
          'appendix-c.md': [657, 658, 659, 660, 661, 662, 663, 664, 665, 666, 668, 669, 670, 671, 672, 673, 674, 675,
                            676, 677, 679, 680, 682, 683, 684, 685, 686, 687, 689, 690, 691, 692, 694, 695, 696, 697,
                            702, 709, 710, 711, 712, 713, 717, 720, 721, 722, 727, 733, 735, 736],
          'appendix-d.md': [745, 754, 755, 757, 763, 764, 772, 775, 778, 779, 780, 781, 784, 789, 801, 802, 805, 806,
                            808, 809, 810, 811, 813, 815, 816, 817]},
 'Shi': {'chapter-02.md': [59]},
 'Gro-f': {'chapter-02.md': [60],
           'chapter-04.md': [198, 201, 220],
           'chapter-05.md': [234, 249, 250, 261, 269, 273],
           'chapter-06.md': [299],
           'appendix-c.md': [662, 664, 665],
           'appendix-d.md': [777, 807, 809]},
 'KG': {'chapter-02.md': [61], 'chapter-09.md': [403], 'appendix-c.md': [665], 'appendix-d.md': [775, 777, 779, 785]},
 'NB': {'chapter-02.md': [61, 62, 72, 73, 85, 103, 104, 111, 114],
        'chapter-04.md': [164, 165, 167, 168, 169, 171, 182, 183, 185, 186, 188, 194, 202, 203, 206, 211, 214, 219,
                          220],
        'chapter-05.md': [222, 227, 228, 229, 231, 235, 244, 245, 246, 248, 249, 250, 255, 256, 267, 272, 278, 279,
                          280, 281, 282, 284, 285],
        'chapter-06.md': [293, 296, 299, 302],
        'chapter-07.md': [327, 328, 330, 335, 344, 346, 350, 363, 371, 372, 375, 376],
        'chapter-08.md': [384],
        'chapter-09.md': [400, 411],
        'chapter-10.md': [440, 443, 445, 457, 460, 462],
        'chapter-11.md': [484],
        'appendix-c.md': [657, 658, 659, 660, 661, 663, 665, 674, 696, 710],
        'appendix-d.md': [808, 809]},
 'Tre': {'chapter-02.md': [61, 62, 69, 70],
         'chapter-03.md': [132],
         'chapter-04.md': [156, 160, 161, 164, 169, 194, 204, 205],
         'chapter-05.md': [235, 244, 245, 246, 247, 248, 249, 253, 254, 255, 263],
         'chapter-06.md': [289],
         'chapter-07.md': [328, 375],
         'chapter-09.md': [430],
         'chapter-10.md': [448, 452, 468, 469],
         'chapter-11.md': [490],
         'appendix-c.md': [657, 660, 661, 662, 663, 676, 677, 678, 679, 680, 681, 683, 684, 685, 686, 687, 688, 689,
                           690, 691, 692, 693, 710, 713, 734, 737],
         'appendix-d.md': [745, 752, 753, 754, 755, 757, 764, 775, 778, 779, 801, 802, 808, 810, 811, 817]},
 'Kothe-I': {'chapter-02.md': [61],
             'chapter-05.md': [227, 243],
             'chapter-10.md': [447, 448],
             'appendix-c.md': [657, 658]},
 'Fol': {'chapter-02.md': [61],
         'chapter-03.md': [140],
         'chapter-04.md': [174, 175, 185],
         'chapter-05.md': [250],
         'chapter-09.md': [396, 398, 399, 401, 405, 407, 410, 411, 413],
         'chapter-10.md': [457, 464],
         'chapter-11.md': [476, 477],
         'chapter-12.md': [501, 504, 506, 509, 511],
         'appendix-a.md': [566, 567, 568, 571, 581, 582, 583, 584, 585],
         'appendix-b.md': [597, 628],
         'appendix-c.md': [710, 711],
         'appendix-d.md': [776, 784]},
 'Bru': {'chapter-02.md': [62, 63, 67, 69],
         'chapter-04.md': [204, 205],
         'chapter-05.md': [238],
         'chapter-09.md': [419],
         'appendix-b.md': [617, 623, 626],
         'appendix-d.md': [745, 758, 760, 763, 764, 777, 819]},
 'DE': {'chapter-02.md': [62, 97],
        'chapter-03.md': [126, 127, 135, 150],
        'chapter-04.md': [175, 177, 179, 185, 195, 196, 207, 209, 210],
        'chapter-06.md': [290, 291, 292, 300],
        'chapter-09.md': [397, 400, 401, 405, 407, 425],
        'chapter-11.md': [477],
        'chapter-12.md': [505, 507, 512],
        'appendix-a.md': [539, 541, 570],
        'appendix-b.md': [629],
        'appendix-c.md': [718],
        'appendix-d.md': [745, 747, 748, 749, 757, 758, 773, 775, 777]},
 'Gro-c': {'chapter-02.md': [69]},
 'Gro-b': {'chapter-02.md': [69, 70, 72],
           'chapter-04.md': [189, 198],
           'appendix-c.md': [663, 680, 682, 683, 685, 689, 719],
           'appendix-d.md': [808, 811]},
 'Bou-GT': {'chapter-02.md': [69],
            'chapter-04.md': [182],
            'chapter-06.md': [289],
            'chapter-08.md': [385, 386],
            'chapter-12.md': [507],
            'appendix-a.md': [571, 572, 583],
            'appendix-c.md': [658, 659],
            'appendix-e.md': [824, 832, 849, 862, 865]},
 'MV': {'chapter-02.md': [72], 'chapter-05.md': [231]},
 'Schm': {'chapter-02.md': [75], 'appendix-a.md': [563, 564]},
 'Davenport-1': {'chapter-02.md': [75], 'appendix-a.md': [562, 563]},
 'Gao': {'chapter-02.md': [75]},
 'RV': {'chapter-02.md': [77, 92, 93],
        'chapter-03.md': [119, 120, 123, 126, 128, 130, 137, 145],
        'chapter-05.md': [273],
        'chapter-07.md': [336, 365],
        'appendix-a.md': [539, 556, 560]},
 'Bou-II': {'chapter-02.md': [96],
            'chapter-04.md': [172, 199],
            'chapter-11.md': [476, 479],
            'chapter-12.md': [504, 505, 506, 507, 509, 510, 511, 512],
            'appendix-a.md': [573],
            'appendix-d.md': [748]},
 'HL': {'chapter-02.md': [110], 'appendix-b.md': [595]},
 'Me': {'chapter-02.md': [113], 'chapter-05.md': [222]},
 'Riemann': {'chapter-03.md': [117, 122]},
 'CPS': {'chapter-03.md': [118], 'chapter-06.md': [302, 309]},
 'IK': {'chapter-03.md': [124, 137], 'appendix-b.md': [590, 636]},
 'Tate': {'chapter-03.md': [124], 'chapter-14.md': [524, 525, 526, 527, 528]},
 'Del': {'chapter-03.md': [124], 'chapter-14.md': [528]},
 'Langlands': {'chapter-03.md': [124], 'chapter-14.md': [525, 526, 527, 530]},
 'T1': {'chapter-03.md': [128], 'appendix-b.md': [589, 590, 644]},
 'H': {'chapter-03.md': [128]},
 'Sarnak': {'chapter-03.md': [137], 'chapter-07.md': [312, 316, 317, 318, 319, 320, 321, 323]},
 'Weil-a': {'chapter-03.md': [142, 151, 153], 'chapter-05.md': [277, 278, 279]},
 'T2': {'chapter-03.md': [145], 'appendix-b.md': [589, 637, 641, 642, 643, 644, 645, 648]},
 'Kudla': {'chapter-03.md': [153]},
 'Kub': {'chapter-04.md': [156], 'appendix-c.md': [697, 698, 701, 703]},
 'BJL': {'chapter-04.md': [156]},
 'Fol-2': {'chapter-04.md': [157]},
 'Carleson': {'chapter-04.md': [157]},
 'Katzn': {'chapter-04.md': [157, 158]},
 'Hunt': {'chapter-04.md': [157]},
 'Kol': {'chapter-04.md': [158]},
 'Lit-II': {'chapter-04.md': [158], 'chapter-07.md': [367], 'chapter-10.md': [453]},
 'Lit-I': {'chapter-04.md': [158], 'appendix-c.md': [694, 696]},
 'Kal': {'chapter-04.md': [158, 159, 170], 'chapter-07.md': [312], 'chapter-10.md': [444, 462]},
 'McAr': {'chapter-04.md': [160, 161]},
 'DyM': {'chapter-04.md': [160]},
 'Apiola': {'chapter-04.md': [164]},
 'MV-2': {'chapter-04.md': [164]},
 'Val-b': {'chapter-04.md': [164, 165]},
 'Gro-e': {'chapter-04.md': [164], 'appendix-c.md': [666, 667, 668, 669, 687]},
 'FlM': {'chapter-04.md': [165, 169], 'appendix-c.md': [668]},
 'Gdm': {'chapter-04.md': [168]},
 'Cnw-b': {'chapter-04.md': [168],
           'chapter-05.md': [227],
           'chapter-07.md': [328, 370],
           'chapter-10.md': [459, 464],
           'appendix-c.md': [703]},
 'Bou-TVS': {'chapter-04.md': [169, 180],
             'chapter-05.md': [254],
             'chapter-09.md': [398, 401, 410],
             'appendix-c.md': [657, 658, 663, 673, 681, 709, 710, 711, 715]},
 'Ru-2': {'chapter-04.md': [170, 171, 172, 173, 207],
          'chapter-09.md': [421, 422],
          'chapter-11.md': [476, 477],
          'appendix-a.md': [581]},
 'Simon': {'chapter-04.md': [173]},
 'Cnw-a': {'chapter-04.md': [176, 177, 179, 185],
           'chapter-05.md': [280, 283],
           'chapter-09.md': [405, 428],
           'chapter-11.md': [481, 482],
           'chapter-12.md': [500, 501],
           'appendix-c.md': [663, 697, 698, 699, 700, 701, 703]},
 'EU': {'chapter-04.md': [176, 177]},
 'HP': {'chapter-04.md': [177]},
 'AS': {'chapter-04.md': [177]},
 'Coh': {'chapter-04.md': [177], 'chapter-09.md': [396]},
 'Bog': {'chapter-04.md': [177], 'appendix-a.md': [572]},
 'AT': {'chapter-04.md': [179], 'chapter-14.md': [525, 526], 'appendix-d.md': [789, 791]},
 'Kn': {'chapter-04.md': [179, 185]},
 'Bou-I': {'chapter-04.md': [186],
           'chapter-12.md': [504, 506, 509, 510, 512],
           'appendix-a.md': [579],
           'appendix-c.md': [711, 712, 714, 715, 717, 718, 720, 721, 722]},
 'SN': {'chapter-04.md': [198, 201, 220],
        'chapter-05.md': [234, 244, 249, 250, 261, 269, 273],
        'chapter-06.md': [299],
        'appendix-c.md': [663]},
 'Kothe-II': {'chapter-04.md': [204], 'chapter-05.md': [243]},
 'Ru-3': {'chapter-04.md': [216, 217]},
 'Me2': {'chapter-05.md': [222, 238]},
 'Me3': {'chapter-05.md': [222, 238]},
 'GE': {'chapter-05.md': [227], 'chapter-07.md': [332], 'appendix-c.md': [719, 742]},
 'HN': {'chapter-05.md': [238]},
 'Horm': {'chapter-05.md': [243, 247], 'chapter-09.md': [423, 425], 'appendix-b.md': [603], 'appendix-d.md': [779]},
 'Val-a': {'chapter-05.md': [244, 248]},
 'Ahl': {'chapter-05.md': [271]},
 'Gro-d': {'chapter-06.md': [293]},
 'Iwaniec': {'chapter-07.md': [312, 319]},
 'Bohr1': {'chapter-07.md': [312]},
 'Bohr2': {'chapter-07.md': [312]},
 'Bohr3': {'chapter-07.md': [312]},
 'Bohr': {'chapter-07.md': [313]},
 'Ba1': {'chapter-07.md': [313, 314], 'appendix-b.md': [632]},
 'Ba2': {'chapter-07.md': [313]},
 'Bohr4': {'chapter-07.md': [313]},
 'Kubota': {'chapter-07.md': [319]},
 'Zagier': {'chapter-07.md': [319]},
 'AtChe': {'chapter-07.md': [320]},
 'BCZ': {'chapter-07.md': [320]},
 'Series': {'chapter-07.md': [320]},
 'Bar': {'chapter-07.md': [327], 'appendix-b.md': [617]},
 'Jor-a': {'chapter-07.md': [332], 'appendix-c.md': [719, 742]},
 'Gro-a': {'chapter-07.md': [366], 'appendix-c.md': [710, 713, 719, 724, 726, 732, 737, 738, 739]},
 'Den': {'chapter-07.md': [373], 'chapter-08.md': [393]},
 'Dur': {'chapter-07.md': [374], 'chapter-09.md': [406, 411], 'appendix-b.md': [592]},
 'GR': {'chapter-09.md': [396, 397], 'appendix-e.md': [889, 898, 899, 900, 901, 902, 903, 905, 906, 921, 922]},
 'FG': {'chapter-09.md': [396]},
 'Ru': {'chapter-09.md': [397], 'appendix-d.md': [745, 746, 747, 793]},
 'Weil-e': {'chapter-09.md': [403],
            'chapter-14.md': [525, 526],
            'appendix-b.md': [622, 625],
            'appendix-d.md': [792, 793]},
 'Yos': {'chapter-09.md': [406]},
 'HR-1': {'chapter-09.md': [424], 'appendix-a.md': [585]},
 'Lang-b': {'chapter-09.md': [425], 'chapter-10.md': [450], 'appendix-b.md': [606, 617, 641, 642]},
 'Bris-a': {'chapter-09.md': [429, 430, 431],
            'chapter-12.md': [500, 501],
            'appendix-a.md': [569],
            'appendix-c.md': [707, 708]},
 'Bris-b': {'chapter-09.md': [429], 'chapter-12.md': [504], 'appendix-a.md': [569], 'appendix-c.md': [707, 708]},
 'Lang-e': {'chapter-10.md': [455]},
 'Meg': {'chapter-10.md': [462]},
 'HR-2': {'chapter-12.md': [498], 'appendix-a.md': [566, 567, 569, 578, 579, 580, 581, 582]},
 'Weil-f': {'chapter-14.md': [525, 526, 528, 531]},
 'Se': {'chapter-14.md': [526]},
 'Art-2': {'chapter-14.md': [528]},
 'Murty': {'chapter-14.md': [528]},
 'Rud-Sa': {'chapter-14.md': [529]},
 'Ru-Sa': {'chapter-14.md': [529, 533]},
 'Arm': {'chapter-14.md': [529]},
 'Ng': {'chapter-14.md': [529]},
 'Goss': {'chapter-14.md': [530, 532]},
 'Omar': {'chapter-14.md': [530]},
 'Quer': {'chapter-14.md': [532]},
 'Silverman': {'chapter-14.md': [532]},
 'JL': {'chapter-14.md': [532]},
 'Moroz': {'chapter-14.md': [533]},
 'KleMo': {'chapter-14.md': [533]},
 'Weil-c': {'appendix-a.md': [541]},
 'Conrad': {'appendix-a.md': [541]},
 'Oes': {'appendix-a.md': [561]},
 'StSha-III': {'appendix-a.md': [567, 568, 579]},
 'HuWe': {'appendix-a.md': [568]},
 'StStr': {'appendix-a.md': [568]},
 'Kech': {'appendix-a.md': [571]},
 'Birkhoff': {'appendix-a.md': [571]},
 'Struble': {'appendix-a.md': [571]},
 'Klee': {'appendix-a.md': [572, 574]},
 'MVe': {'appendix-b.md': [589]},
 'Neu': {'appendix-b.md': [590, 591]},
 'Nik': {'appendix-b.md': [592]},
 'Weil-b': {'appendix-b.md': [606, 615, 617]},
 'Lang-a': {'appendix-b.md': [617]},
 'CFSS': {'appendix-b.md': [626]},
 'HK': {'appendix-b.md': [626, 627]},
 'Hu1': {'appendix-b.md': [626, 627, 628]},
 'Hu2': {'appendix-b.md': [626, 631]},
 'Mit': {'appendix-b.md': [635]},
 'MVa': {'appendix-b.md': [637]},
 'SW': {'appendix-b.md': [637]},
 'Ingh3': {'appendix-b.md': [637, 638, 639]},
 'Lang-c': {'appendix-b.md': [640]},
 'QQ': {'appendix-b.md': [644]},
 'HW': {'appendix-b.md': [653]},
 'GL': {'appendix-b.md': [653]},
 'Sm': {'appendix-c.md': [659]},
 'Cl': {'appendix-c.md': [659]},
 'Ba': {'appendix-c.md': [659]},
 'Pa': {'appendix-c.md': [666]},
 'Ret': {'appendix-c.md': [666]},
 'Vogt-1': {'appendix-c.md': [666, 667], 'appendix-d.md': [765]},
 'DS': {'appendix-c.md': [666, 711]},
 'Wngr-2': {'appendix-c.md': [668], 'appendix-d.md': [764]},
 'BKMcK': {'appendix-c.md': [670]},
 'Voigt': {'appendix-c.md': [674, 712]},
 'Ch': {'appendix-c.md': [677]},
 'Cnw-c': {'appendix-c.md': [697, 698, 702, 707]},
 'Ryan': {'appendix-c.md': [705]},
 'Arthur': {'appendix-c.md': [708]},
 'Lang-d': {'appendix-c.md': [710], 'appendix-d.md': [747]},
 'Za': {'appendix-c.md': [711]},
 'DU': {'appendix-c.md': [711, 714]},
 'Kruse': {'appendix-c.md': [719, 723, 724, 725, 726, 728, 741]},
 'BJM': {'appendix-c.md': [719, 742]},
 'Sch-b': {'appendix-c.md': [732, 734, 735, 736]},
 'Ga-2': {'appendix-c.md': [732]},
 'Dunford': {'appendix-c.md': [739]},
 'Jor-b': {'appendix-c.md': [741]},
 'Wa': {'appendix-d.md': [745, 759, 768, 773, 787]},
 'Au': {'appendix-d.md': [766]},
 'Al-B': {'appendix-d.md': [778]},
 'Wrn': {'appendix-d.md': [786]},
 'HKZ': {'appendix-d.md': [799]},
 'Du': {'appendix-e.md': [824, 835, 853, 861]},
 'Ke': {'appendix-e.md': [824, 826, 835]},
 'SP': {'appendix-e.md': [824, 825, 832, 834, 835, 840, 847, 868, 869, 872, 873, 874, 880, 881, 882, 883, 886, 889,
                          892, 894, 898, 900, 906, 920, 921, 922, 923, 924, 925, 926, 929]},
 'LGL': {'appendix-e.md': [824, 825, 826, 827, 828, 833, 835, 836, 837, 841, 842, 846, 861]},
 'Rezk': {'appendix-e.md': [824, 825, 826, 827, 828, 833, 835, 836, 837, 846, 847, 848]},
 'Ste': {'appendix-e.md': [824, 825, 826, 827, 828, 835, 837, 861]},
 'Str': {'appendix-e.md': [825, 826, 827, 828, 833, 834, 835, 836, 837, 841, 842, 843, 844, 846, 847, 848, 851, 852,
                           854, 855, 856, 862]},
 'Br4': {'appendix-e.md': [825, 842]},
 'BG': {'appendix-e.md': [825]},
 'LMS': {'appendix-e.md': [825]},
 'May': {'appendix-e.md': [825]},
 'Br1': {'appendix-e.md': [825, 826]},
 'Br2': {'appendix-e.md': [825, 826]},
 'Br3': {'appendix-e.md': [825, 826]},
 'Vogt': {'appendix-e.md': [826]},
 'Ga': {'appendix-e.md': [826]},
 'nLab1': {'appendix-e.md': [826]},
 'MacL': {'appendix-e.md': [826, 834, 835, 836, 837, 841]},
 'ELS': {'appendix-e.md': [826, 828, 833, 835, 836, 837]},
 'McC': {'appendix-e.md': [826, 827, 828, 833, 846]},
 'LM': {'appendix-e.md': [826]},
 'Jech': {'appendix-e.md': [831, 832, 836, 868, 869, 873]},
 'Kunen': {'appendix-e.md': [831, 868, 869, 873, 876, 878]},
 'StSe': {'appendix-e.md': [833, 843, 848, 861, 866, 867]},
 'Kel': {'appendix-e.md': [834]},
 'EK': {'appendix-e.md': [835, 841]},
 'MacL2': {'appendix-e.md': [835]},
 'Bor2': {'appendix-e.md': [841, 842, 862, 865]},
 'Fr': {'appendix-e.md': [843, 844]},
 'ABM': {'appendix-e.md': [844]},
 'PB': {'appendix-e.md': [848]},
 'VLH': {'appendix-e.md': [850]},
 'vO': {'appendix-e.md': [865, 878, 879]},
 'KS': {'appendix-e.md': [880, 881, 882]},
 'SGA3': {'appendix-e.md': [882]},
 'Les': {'appendix-e.md': [882]},
 'SGA4': {'appendix-e.md': [882, 886]},
 'Hig': {'appendix-e.md': [883]},
 'CdSW': {'appendix-e.md': [883]},
 'N': {'appendix-e.md': [883]},
 'Be': {'appendix-e.md': [889, 900]},
 'Mar': {'appendix-e.md': [889]},
 'Ehr1': {'appendix-e.md': [889]},
 'Ehr2': {'appendix-e.md': [889]},
 'Bor1': {'appendix-e.md': [889, 898, 900, 903]},
 'Ha': {'appendix-e.md': [889, 898, 900, 905]},
 'Ac': {'appendix-e.md': [920, 921]}}
# the keys no bracketed citation names
UNCITED = ['AB', 'ABR', 'Ara', 'Art-1', 'Aub', 'BB', 'BCR', 'BGV', 'BJ', 'Bl', 'BL', 'Bo', 'Bou', 'BT', 'Car', 'Cha', 'CHR',
 'Davenport-2', 'De', 'De2', 'De3', 'De4', 'DiM', 'Dix', 'E', 'EGAI', 'EGAII', 'EGAIII$_1$', 'EGAIII$_2$',
 'EGAIV$_1$', 'EGAIV$_2$', 'EGAIV$_3$', 'EGAIV$_4$', 'FGT', 'FK', 'Flo', 'FM', 'For', 'FSt', 'FujKa', 'Ga-1', 'Gle',
 'GNar', 'GoKre', 'GRa', 'GrM', 'Hor', 'HS', 'HSS', 'HSt', 'Ingh1', 'Ingh2', 'Iw', 'JPP', 'Ka', 'Kakutani', 'Ke-a',
 'Ke-b', 'Kob', 'TKYK', 'La', 'Lang-f', 'LR', 'Lee', 'LT', 'M', 'Mat-I', 'Mat-II', 'Mi', 'MLei', 'Mos', 'Mu', 'MZ',
 'Pinsky', 'Ro', 'RS', 'SGA1', 'SO', 'TsV', 'VK', 'Vogt-2', 'Vor', 'Weil-d', 'W', 'Wi', 'Wil', 'Wngr-1', 'Yos-2']

# the Stacks project's tags its citations name -> the pages citing each, in the order first cited
SP_TAGS = {'004O': [824],
 '0405': [824],
 '08ZD': [824],
 '0059': [824],
 '08ZQ': [824],
 '005M': [824, 840],
 '08ZW': [824],
 '0908': [824],
 '0406': [825],
 '08ZK': [832],
 '08ZT': [834],
 '08ZI': [835],
 '08ZJ': [835],
 '005P': [847],
 '046U': [868],
 '000H': [868],
 '05N1': [868],
 '000B': [868, 869],
 '00VG': [868],
 '00UZ': [868],
 '000I': [872],
 '000J': [873, 874],
 '000P': [874],
 '00VH': [880, 881],
 '000W': [881],
 '00YW': [881],
 '00YZ': [881, 882],
 '00Z1': [881],
 '00Z4': [882],
 '00Z6': [882],
 '02YB': [882],
 '000X': [882],
 '00VY': [882],
 '00ZA': [882],
 '00Z8': [882],
 '00Z9': [882],
 '022L': [883],
 '0437': [883],
 '00V1': [886],
 '001O': [886],
 '003G': [889, 900],
 '003O': [889, 900],
 '003D': [889, 892],
 '001K': [894],
 '003F': [894],
 '003H': [898],
 '003J': [898],
 '02XG': [900],
 '02XP': [900],
 '02XQ': [900],
 '003L': [900],
 '003N': [906],
 '0026F': [920],
 '003V': [921],
 '02Y2': [921, 924],
 '02XW': [921],
 '004A': [921],
 '02ZB': [922],
 '026F': [922],
 '001P': [922],
 '02Y1': [923],
 '04S8': [923],
 '04SF': [923],
 '04Z2': [924],
 '034I': [924],
 '034H': [924, 926],
 '042H': [925],
 '04Z3': [925],
 '06PB': [926],
 '06NS': [926],
 '046S': [929],
 '044V': [929],
 '046T': [929],
 '046N': [929]}

W = 2400
STACKS = "SP"                       # the key of the Stacks project, whose citations name its tags
TAG = re.compile(r"[0-9A-Z]{4}")
PAPERS = pathlib.Path(__file__).resolve().parent / "papers.toml"
HOSTS = [("https://doi.org/", "DOI"), ("https://zbmath.org/", "zbMATH"), ("https://arxiv.org/", "arXiv"),
         ("http://www.numdam.org/", "numdam"), ("https://www.numdam.org/", "numdam"), ("https://eudml.org/", "EuDML"),
         ("http://eudml.org/", "EuDML"), ("https://stacks.math.columbia.edu/", "Stacks project"),
         ("https://topology.pi-base.org/", "pi-Base"), ("https://www.claymath.org/", "Clay Institute")]


def ident(r):
    return r.key if r.n == 1 else f"{r.key} ({r.n})"


def host(url):
    for prefix, name in HOSTS:
        if url.startswith(prefix):
            return name
    raise ValueError(f"diagrams/src/papers.toml links {url}, on a host B1 does not name (HOSTS)")


def sources(m):
    return (f"riemann-masullo ({rm.URL}) at {rm.SHORT} ({m.date}): transcription/README.md and "
            f"transcription/chapters/, its transcription of the manuscript, and paper/README.md; diagrams/src/deps.json "
            f"for the cards' pages; diagrams/src/papers.toml, this repository's links to the works "
            f"(tools/link-papers.py). riemann-masullo-diagrams is independent of riemann-masullo and not maintained "
            f"by it.")


def read():
    P = paper.load()
    pages = P.pages()
    return P, {"REFERENCES": [ident(r) for r in P.refs], "CITED": pages,
               "UNCITED": [k for k in dict.fromkeys(r.key for r in P.refs) if k not in pages],
               "SP_TAGS": P.tags(STACKS)}


def tag_url(t):
    return f"https://stacks.math.columbia.edu/tag/{t}"


def build():
    m = rm.load()
    P, got = read()
    rm.require("REFERENCES", REFERENCES, got["REFERENCES"], "B1's rows against the transcription's bibliography")
    rm.require("CITED", CITED, got["CITED"], "B1's last column against the citations in the transcription's text")
    rm.require("UNCITED", UNCITED, got["UNCITED"], "B1's rows cited nowhere against the transcription's text")
    rm.require("SP_TAGS", SP_TAGS, got["SP_TAGS"], f"B1's row of [{STACKS}] against its citations' tags")
    if "Stacks Project" not in P.by_key[STACKS][0].plain:
        raise ValueError(f"the bibliography's [{STACKS}] is no longer the Stacks project: re-read B1's STACKS")
    papers = tomllib.loads(PAPERS.read_text(encoding="utf-8"))
    ids = got["REFERENCES"]
    missing = [i for i in ids if i not in papers]
    extra = [i for i in papers if i not in ids]
    if missing or extra:
        raise ValueError(f"diagrams/src/papers.toml: no entry for {missing}; entries naming no bibliography entry "
                         f"{extra}: add or remove them (proof-posters:linking-papers, tools/link-papers.py)")
    for i, e in papers.items():
        if e.get("via") not in ("crossref", "zbmath", "hand", "none") or (e["via"] == "none") == ("url" in e):
            raise ValueError(f"diagrams/src/papers.toml: [{i!r}] needs a url and a via, or via = \"none\" and no url")
        if e["via"] in ("hand", "none") and not e.get("note"):
            raise ValueError(f"diagrams/src/papers.toml: [{i!r}] is via = {e['via']!r} and has no note")
    lib.PAPERS.update({i: e["url"] for i, e in papers.items() if "url" in e})
    lib.PAPERS.update({f"{STACKS} tag {t}": tag_url(t) for t in got["SP_TAGS"] if TAG.fullmatch(t)})

    X = I.load()
    chapters = {it.chapter for it in X.items.values()}
    by_chapter = collections.defaultdict(list)
    for it in X.items.values():
        by_chapter[it.chapter].append(it)
    of_file = {f: paper.chapter_of_file(f, chapters) for f in paper.FILES}
    n_cites = collections.Counter(c.key for c in P.cites)
    doubled = sorted(k for k, v in P.by_key.items() if len(v) > 1)
    n_pages = len({c.page for c in P.cites})
    linked = sum(1 for e in papers.values() if "url" in e)
    via = collections.Counter(e["via"] for e in papers.values())

    c = lib.Canvas(
        ID, "The works the manuscript cites, and where",
        f"The bibliography of the manuscript, pp. {P.refs[0].page}–{P.refs[-1].page}, as riemann-masullo transcribes it "
        f"at {rm.SHORT}: {len(P.refs)} entries under {len(P.by_key)} keys. Its text cites {len(got['CITED'])} of "
        f"them, {len(P.cites):,} times, on {n_pages:,} of its pages; {len(got['UNCITED'])} are cited nowhere in "
        f"brackets. "
        f"{linked} entries link to the work.", W, sources(m), state=rm.state(m))
    x0, x1 = c.x0, c.x1
    y = c.y
    y += draw.nav(c, ID, y)
    y += c.para(x0, y, x1 - x0,
                "**How to read it.** One row per entry of the bibliography, in the order printed. The entry is "
                "riemann-masullo's transcription of it: the work's authors, title, venue and year, as printed, the "
                "emphasis dropped and mathematics shown as written. A citation is a bracketed key in the text, such as "
                "[NB, Thm.14.4.5(b)], read outside formulas, on the page its `PDF page` marker gives. A cited page "
                "opens the card on its chapter poster whose `Paper:` pages cover it, the card with the fewest "
                "pages where several do; a page no card covers is not a link. These are the paper's citations. The "
                "Lean cites none of these works: no docstring or comment of riemann-masullo's Lean names a key, and "
                "nothing here says that the Lean rests on a work, or that the paper uses it rightly.", size=14.5,
                color="muted") + 14
    y += c.para(x0, y, x1 - x0,
                f"**The links** are this repository's, not the manuscript's (diagrams/src/papers.toml): "
                f"{via['crossref']} found on Crossref and checked against the DOI's own record, {via['zbmath']} on "
                f"zbMATH Open, {via['hand']} settled by hand, and {via['none']} found by neither, drawn without one. "
                f"An entry with a link opens the work too, as its Link column does. "
                f"A link is to the work the entry names, matched on its title, first author and year; that it is the "
                f"edition the manuscript used is not checked. The Stacks project's tags its citations name each open "
                f"the tag's page there, a tag being stable by the project's design; that a tag says what the "
                f"manuscript cites it for is not checked."
                + (f" The bibliography prints two entries under each of {', '.join('[' + k + ']' for k in doubled)}; "
                   f"a citation cannot tell them apart, and is drawn under both." if doubled else ""),
                size=14.5, color="muted") + 26

    cols = [("Key", 170), ("The entry, as the transcription prints it", 1010), ("Link", 170), ("Cited", 90),
            ("Where the text cites it: chapter, and each page", 848)]
    rows = []
    for r in P.refs:
        where = []
        for f, pgs in got["CITED"].get(r.key, {}).items():
            ch = of_file[f]
            parts = []
            for pg in pgs:
                card = paper.card_of_page(by_chapter.get(ch, []), pg) if ch else None
                parts.append(draw.to_poster(CH.poster_id(ch), str(pg), anchor=card.anchor) if card else str(pg))
            label = paper.file_label(f)
            head = draw.to_poster(CH.poster_id(ch), label) if ch else label
            where.append(f"{head}: {'p.' if len(pgs) == 1 else 'pp.'} {', '.join(parts)}")
        if r.key == STACKS and got["SP_TAGS"]:
            tags = [(draw.to_url(tag_url(t), t) if TAG.fullmatch(t) else f"{t} (not a tag's form, so not a link)")
                    + f" ({'p.' if len(pgs) == 1 else 'pp.'} {', '.join(map(str, pgs))})"
                    for t, pgs in got["SP_TAGS"].items()]
            where.append(f"the tags cited, each opening its page on the Stacks project: {', '.join(tags)}")
        e = papers[ident(r)]
        text, cut = draw.coverable(r.plain)
        if "url" in e:              # the entry opens the work, as its Link column does
            text = draw.to_url(e["url"], text)
        rows.append({"cells": [f"[{r.key}]" + (f" ({r.n})" if r.n > 1 else ""),
                               text + (" (abridged: the rest uses a character the fonts lack)" if cut else ""),
                               draw.to_url(e["url"], host(e["url"])) if "url" in e else "none found",
                               f"{n_cites[r.key]}" if n_cites[r.key] else "none",
                               "; ".join(where) or "cited nowhere in brackets"],
                     "anchor": r.anchor,
                     "accent": None if n_cites[r.key] else "grey"})
    y += c.table(x0, y, cols, rows, size=12, hsize=12.5, pad=6)
    y += 26
    y += c.para(x0, y, x1 - x0,
                "**What this does not say.** Nothing was built or proved here, and the PDF was not read: the entries "
                "and citations are read from riemann-masullo's transcription at the pin, which names the PDF by the "
                "hash PAPER_SHA256 pins. The transcription was checked against the PDF by scripts and AI reviewers, "
                "not read symbol by symbol by a person (its README); a misread key is a misdrawn citation. A work "
                "cited in other words than a bracketed key is not counted. That a work says what the manuscript "
                "cites it for was not checked, and the linked works were not read.", size=13.5, color="muted")
    return c
