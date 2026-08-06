import os

def main_menu():
    while True:
        print("\n" + "=" * 50)
        print("🚀 GrowthEngine Master Control Center")
        print("=" * 50)
        print("1. Run Full Pipeline")
        print("2. Search & Query Database")
        print("3. Financial Analytics & Reports")
        print("4. Export Executive Report")
        print("5. Exit System")
        print("=" * 50)

        choice = input("Enter your choice (1 to 5): ").strip()

        if choice == '1':
            print("\n--- Running Full Pipeline ---")
            os.system("python main.py")
        elif choice == '2':
            print("\n--- Opening Search Engine ---")
            os.system("python search.py")
        elif choice == '3':
            print("\n--- Calculating Financial Analytics ---")
            os.system("python analytics.py")
        elif choice == '4':
            print("\n--- Exporting Executive Report ---")
            os.system("python reports.py")
        elif choice == '5':
            print("\nExiting system. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main_menu()