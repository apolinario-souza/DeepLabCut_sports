# Application of the DeepLabCut Toolbox in Sports: A Deep Learning Approach

Apolinário-Souza, T., Bedo, B. L. S., Leonardi, T. J. Application of the DeepLabCut toolbox in sports: a Deep Learning approach. 2024



![Descrição do GIF](https://github.com/apolinario-souza/DeepLabCut_sports/blob/main/gif_video.gif)


## This repository contains the online materials for the article

[Original video](https://github.com/apolinario-souza/DeepLabCut_sports/blob/main/hand.mp4)

[Video with DeepLabCut](https://github.com/apolinario-souza/DeepLabCut_sports/blob/main/Game-hand-2024-08-11/videos/handDLC_resnet50_GameAug11shuffle1_5000_labeled.mp4)

[Tutorial video 1](https://youtu.be/7Prv_8zBTi4)

[Script 1](https://github.com/apolinario-souza/DeepLabCut_sports/blob/main/script_1.py)

[How to Install DeepLabCut](https://github.com/apolinario-souza/DeepLabCut_sports/blob/main/How_to_Install_DeepLabCut.pdf)

[Script 2](https://github.com/apolinario-souza/DeepLabCut_sports/blob/main/script_2.ipynb)

[Script 3](https://github.com/apolinario-souza/DeepLabCut_sports/blob/main/script_3.ipynb)


# Flowchart of the Implementation of the DeepLabCut Algorithm

```mermaid
graph TD;
    A(Start) --> B[Video_capture]
    B --> C[Pre-process_video]
    C --> D[Remove_ball-out]
    C --> E[Select_frames]
    D --> F[Manual_annotation]
    E --> F
    F --> G[Annotate:_players_ball_cones]
    G --> H[Create_training_dataset]
    H --> I[Apply_data_augmentation]
    I --> J[Train_neural_network]
    J --> K[Monitor_loss]
    K --> L[Evaluate_model]
    L --> M[Compute_Euclidean_error]
    M --> N[Apply_perspective_transform]
    N --> O[Compute_homography_matrix]
    O --> P[Filter_tracked_data]
    P --> Q[Remove_low-confidence_points]
    Q --> R[Apply_position_constraints]
    R --> S[Analyze_movement_patterns]
    S --> T[Assess_accuracy]
    T --> U(End)

    
    
```


