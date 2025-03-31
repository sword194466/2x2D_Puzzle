# 2x2D_Puzzle
## Generation logic
The puzzle generation process is the following (consider one of the layers):
1. generate base grid:

   ![image](https://github.com/user-attachments/assets/170ca4ee-2982-4144-9945-f403bb917054)
   
3. define playable area (anywhere out of the inner box will be considered out of bounds):

   ![image](https://github.com/user-attachments/assets/edafd320-d5dc-4d70-8782-e59e4522ef10)
   
5. use 5x5 blocks to parse through the playable area (try to cover as much as possible)
   where each cell of each block has a 0.5 chance to take on the label of the piece
   
   ![image](https://github.com/user-attachments/assets/d7bdc9aa-b991-4746-b6f5-fba0e9c1f861)

   labels are randomized repeated letters (i.e. the first piece can be labelled with "bb")

   ![image](https://github.com/user-attachments/assets/7b65c8b1-16d7-4748-aa5c-75fa4ba29b0b)
   
7. note that in step 3 there may still be empty spaces, parse again with 7x7 blocks
   with each block filling up spaces in its area
   
   ![image](https://github.com/user-attachments/assets/fba9c5b4-6977-473e-a194-dbd50e3123f7)
   
9. randomize the generated puzzle array again


## Execution (without download)
1. select the HTML game file and click on <raw>

![image](https://github.com/user-attachments/assets/1de28854-9ed1-4f78-a492-f179348a4be3)

2. replace <raw.githubusercontent.com> to <raw.githack.com> and the game should be running
   
   ![image](https://github.com/user-attachments/assets/1bbd7b85-a73f-48ae-9145-71cdc6e403aa)

## Execution (download)
1. download the HTML file and execute
