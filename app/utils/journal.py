from app.db.models import PageModel


def evaluate_streak(new_page: PageModel, last_page: PageModel, current_streak: int)-> int:
    delta = new_page.submitted - last_page.submitted
    
    if delta.days == 1 :
        return current_streak + 1
    return 0