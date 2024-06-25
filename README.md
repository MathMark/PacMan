# Pacman

Old classic Pacman game written in Python using pygame library.

## Ghosts behaviour

| Name   | Description  | Behaviour                                                                                                                                                                                                                                                               |
|--------|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Blinky | Red Ghost    | Follows Pac-Man directly during Chase mode, and heads to the upper-right corner during Scatter mode.                                                                                                                                                                    |
| Pinky  | Pink ghost   | Chases towards the spot 2 Pac-Dots in front of Pac-Man. Due to a bug in the original game's coding, if Pac-Man faces upwards, Pinky's target will be 2 Pac-Dots in front of and 2 to the left of Pac-Man. During Scatter mode, she heads towards the upper-left corner. |
| Inky   | Blue ghost   | During Chase mode, his target is a bit complex. His target is relative to both Blinky and Pac-Man, where the distance Blinky is from Pinky's target is doubled to get Inky's target. He heads to the lower-right corner during Scatter mode.                            |
| Clyde  | Yellow ghost | Chases directly after Pac-Man, but tries to head to his Scatter corner when within an 8-Dot radius of Pac-Man. His Scatter Mode corner is the lower-left.                                                                                                               |
