from categorization import list_urls, add_url, update_url, delete_url


def main():
    print("SecureGate Proxy CLI")
    while True:
        print("\n1. List URLs\n2. Add URL\n3. Update URL\n4. Delete URL\n5. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            for row in list_urls():
                print(f"ID: {row[0]}, URL: {row[1]}, Category: {row[2]}")

        elif choice == '2':
            url = input("Enter URL (http://example.com): ")
            category = input("Category (ALLOW/BLOCK): ")
            add_url(url, category.upper())

        elif choice == '3':
            url = input("Enter URL to update: ")
            new_cat = input("New Category (ALLOW/BLOCK): ")
            update_url(url, new_cat.upper())

        elif choice == '4':
            url = input("Enter URL to delete: ")
            delete_url(url)

        elif choice == '5':
            break

if __name__ == '__main__':
    main()
