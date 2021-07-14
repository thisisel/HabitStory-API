from app.db.models import PageModel


def evaluate_streak(new_page: PageModel, last_page: PageModel, current_streak: int)-> int:
    delta = new_page.submitted - last_page.submitted
    new_streak = current_streak
    
    if delta.days == 1 :
        new_streak += 1
    if delta.days >= 3:
        new_streak = current_streak -1 if current_streak != 0 else 0
   
    return new_streak