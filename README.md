# 2x2D_Puzzle
The puzzle generation process is the following (consider one of the layers):
1. generate base grid:
   ![image](https://github.com/user-attachments/assets/170ca4ee-2982-4144-9945-f403bb917054)
2. define playable area (anywhere out of the inner box will be considered out of bounds):
   ![image](https://github.com/user-attachments/assets/edafd320-d5dc-4d70-8782-e59e4522ef10)
3. use 5x5 blocks to parse through the playable area (try to cover as much as possible)
   where each cell of each block has a 0.5 chance to take on the label of the piece
   ![image](https://github.com/user-attachments/assets/d7bdc9aa-b991-4746-b6f5-fba0e9c1f861)

   labels are randomized repeated letters (i.e. the first piece can be labelled with "bb")
   ![image](https://github.com/user-attachments/assets/7b65c8b1-16d7-4748-aa5c-75fa4ba29b0b)
5. note that in step 3 there may still be empty spaces, parse again with 7x7 blocks
   with each block filling up spaces in its area
   ![image](https://github.com/user-attachments/assets/fba9c5b4-6977-473e-a194-dbd50e3123f7)
6. randomize the generated puzzle array again






