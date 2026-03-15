import json
import os

DB_FILE = 'data/courses.json'
CONFIG_FILE = 'data/site_config.txt'
TEMPLATE_DIR = 'templates'
OUTPUT_DIR = 'courses' # <-- The new home for your course pages

def ensure_folders():
    """Automatically creates the folder structure."""
    os.makedirs('data', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    os.makedirs('assets/images', exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True) # Creates the new courses folder

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_db(db):
    with open(DB_FILE, 'w') as f:
        json.dump(db, f, indent=4)

def load_config():
    config = {}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            for line in f:
                if '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    return config

def build_site(db):
    print("\n[+] Rebuilding website...")
    config = load_config()
    
    try:
        with open(os.path.join(TEMPLATE_DIR, 'index-template.html'), 'r') as f:
            index_template = f.read()
        with open(os.path.join(TEMPLATE_DIR, 'course-template.html'), 'r') as f:
            course_template = f.read()
    except FileNotFoundError:
        print(f"[-] Error: Make sure index-template.html and course-template.html exist inside '{TEMPLATE_DIR}'!")
        return

    cards_html = ""

    for course_id, data in db.items():
        # Storefront Card: Notice the href now points to the courses/ folder
        card = f"""
        <div class="course-card">
            <img src="{data['img_link']}" alt="{data['title']}" class="course-image">
            <div class="course-info">
                <h3>{data['title']}</h3>
                <p>{data['short_desc']}</p>
                <a href="{OUTPUT_DIR}/course-{course_id}.html" class="btn btn-primary btn-full" style="margin-top: auto;">View Course</a>
            </div>
        </div>
        """
        cards_html += card

        # Handle local image paths smartly for the subfolder
        course_img = data['img_link']
        if not course_img.startswith('http') and not course_img.startswith('../'):
            course_img = '../' + course_img # Fixes the path dynamically!

        # Build Individual Course Page
        page_html = course_template
        page_html = page_html.replace('{{SITE_NAME}}', config.get('SITE_NAME', 'The Studio.'))
        page_html = page_html.replace('{{FOOTER_TEXT}}', config.get('FOOTER_TEXT', '© 2026 The Studio.'))
        page_html = page_html.replace('{{TITLE}}', data['title'])
        page_html = page_html.replace('{{SHORT_DESC}}', data['short_desc'])
        page_html = page_html.replace('{{LONG_DESC}}', data['long_desc'])
        page_html = page_html.replace('{{PRICE}}', data['price'])
        page_html = page_html.replace('{{YT_LINK}}', data['yt_link'])
        page_html = page_html.replace('{{IMG_LINK}}', course_img)
        page_html = page_html.replace('{{PAYMENT_LINK}}', data['payment_link'])

        # Save to the new courses folder
        file_path = os.path.join(OUTPUT_DIR, f'course-{course_id}.html')
        
        if os.path.exists(file_path):
            print(f"  -> Skipped {file_path} (Protected to preserve manual changes)")
        else:
            with open(file_path, 'w') as f:
                f.write(page_html)
            print(f"  -> Generated {file_path}")

    # Generate Main Index Page to root
    final_index = index_template
    final_index = final_index.replace('{{SITE_NAME}}', config.get('SITE_NAME', 'The Studio.'))
    final_index = final_index.replace('{{HERO_TITLE}}', config.get('HERO_TITLE', 'The Studio.'))
    final_index = final_index.replace('{{HERO_SUBTITLE}}', config.get('HERO_SUBTITLE', 'Master your craft.'))
    final_index = final_index.replace('{{FOOTER_TEXT}}', config.get('FOOTER_TEXT', '© 2026 The Studio.'))
    final_index = final_index.replace('{{COURSE_CARDS}}', cards_html)
    
    with open('index.html', 'w') as f:
        f.write(final_index)
    print("  -> Generated index.html")
    print("[+] Site build complete!\n")

def main():
    ensure_folders()
    db = load_db()
    
    while True:
        print("\n=== COURSE MANAGER ===")
        print("1. Add a Course")
        print("2. Remove a Course")
        print("3. List Courses")
        print("4. Rebuild Website")
        print("5. Exit")
        
        choice = input("Select an option: ")
        
        if choice == '1':
            course_id = input("Enter a unique short ID (e.g., python-basics): ").strip().lower()
            title = input("Title: ")
            short_desc = input("Short description: ")
            
            print("\nLong description (type 'DONE' on a new line when finished):")
            lines = []
            while True:
                line = input()
                if line.strip().upper() == 'DONE':
                    break
                lines.append(line)
            long_desc = "\n".join(lines)
            
            price = input("Price (e.g., 49): ")
            yt_link = input("YouTube Embed URL: ")
            img_link = input("Image Path (e.g., assets/images/course1.jpg): ")
            payment_link = input("Razorpay Payment Link: ")
            
            db[course_id] = {
                'title': title, 'short_desc': short_desc, 'long_desc': long_desc,
                'price': price, 'yt_link': yt_link, 'img_link': img_link, 'payment_link': payment_link
            }
            save_db(db)
            print(f"\n[+] '{title}' saved to database.")
            build_site(db)
            
        elif choice == '2':
            course_id = input("Enter the ID of the course to remove: ").strip().lower()
            if course_id in db:
                del db[course_id]
                save_db(db)
                file_path = os.path.join(OUTPUT_DIR, f'course-{course_id}.html')
                if os.path.exists(file_path):
                    os.remove(file_path)
                print(f"\n[+] Course removed.")
                build_site(db)
            else:
                print("\n[-] Course ID not found.")
                
        elif choice == '3':
            print("\n--- Current Courses ---")
            for cid, data in db.items():
                print(f"ID: {cid} | Title: {data['title']}")
                
        elif choice == '4':
            build_site(db)
            
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()