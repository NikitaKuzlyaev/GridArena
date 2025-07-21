from core.api.v1.routers.auth import router as auth_router
from core.api.v1.routers.contest import router as contest_router
from core.api.v1.routers.ping import router as ping_router
from core.api.v1.routers.problem import router as problem_router
from core.api.v1.routers.problem_card import router as problem_card_router
from core.api.v1.routers.quiz_field import router as quiz_field_router
from core.api.v1.routers.submission import router as submission_router
from core.api.v1.routers.contestant import router as contestant_router
from core.api.v1.routers.selected_problem import router as selected_problem_router

routers = [ping_router, auth_router, contest_router, quiz_field_router,
           problem_card_router, problem_router, submission_router, contestant_router, selected_problem_router, ]
