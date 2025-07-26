from visualization import HanoiVisualization

def get_user_input():
    while True:
        try:
            num_disks = int(input("Enter number of disks (1-8): "))
            if 1 <= num_disks <= 8:
                return num_disks
            print("Please enter a number between 1 and 8")
        except ValueError:
            print("Please enter a valid number")

if __name__ == "__main__":
    num_disks = get_user_input()
    visualization = HanoiVisualization(num_disks)
    visualization.run()
