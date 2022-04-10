mmo = input("inp> ")
if len(mmo) <= 2:
    items = {
        '3': 'username',
        '4': 'profile_id',
        '5': 'is_private',
        '6': 'followed_by_viewer',
        '7': 'mediacount',
        '8': 'igtv_count',
        '9': 'followers',
        '1': 'followees',
        '12': 'external_url',
        '13': 'is_business_account',
        '14': 'business_category_name',
        '15': 'biography',
        '16': 'blocked_by_viewer',
        '17': 'follows_viewer',
        '18': 'full_name',
        '19': 'has_blocked_viewer',
        '20': 'has_highlight_reels',
        '21': 'has_public_story',
        '22': 'has_viewable_story',
        '23': 'has_requested_viewer',
        '24': 'is_verified',
        '25': 'requested_by_viewer',
        '26': 'profile_pic_ur'
    }

    print(items[mmo])
