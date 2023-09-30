import multiprocessing as mp

CPU_cores = 3
names = [
    "Alice", "Aiden", "Abigail", "Andrew", "Bella", "Benjamin", "Charlotte", "Caleb", "Chloe", "Daniel",
    "Ella", "Elijah", "Emily", "Ethan", "Grace", "Gabriel", "Hannah", "Henry", "Isabella", "Isaac",
    "Jacob", "Liam", "Lily", "Lucas", "Madison", "Mia", "Mason", "Natalie", "Noah", "Olivia",
    "Oliver", "Sophia", "Samuel", "Sofia", "Sebastian", "Scarlett", "Thomas", "Victoria", "William", "Zoe",
    "Ava", "Alexander", "Addison", "Aaron", "Aria", "Adam", "Amelia", "Anthony", "Avery", "Austin",
    "Brooklyn", "Brandon", "Brianna", "Cameron", "Claire", "Carter", "Evelyn", "Christopher", "Ella", "David",
    "Grace", "Dylan", "Haley", "Eli", "Hannah", "Evan", "Harper", "Jack", "Katherine", "Jackson",
    "Layla", "James", "Lillian", "John", "Lily", "Joseph", "Madison", "Joshua", "Natalie", "Justin",
    "Olivia", "Kevin", "Sophia", "Leah", "William", "Luke", "Zoe", "Michael", "Mila", "Nathan",
    "Nora", "Nicholas", "Penelope", "Owen", "Riley", "Robert", "Zoey", "Samuel", "Sarah", "Tyler",
]
def say_HEllo(name):
    print(f'Hello {name}!')

def main():
    with mp.Pool(CPU_cores) as p:
        # p.map(target, data)
        p.map(say_HEllo, names)
if __name__ == "__main__":
    main()