import reflex as rx


def index() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "sparkles",
                        class_name="h-6 w-6 text-blue-600",
                    ),
                    class_name="flex h-12 w-12 items-center justify-center rounded-2xl bg-blue-50",
                ),
                rx.el.div(
                    rx.el.span(
                        rx.icon("circle-check", class_name="h-3.5 w-3.5"),
                        "运行中",
                        class_name="flex w-fit items-center gap-1.5 rounded-full bg-green-50 px-3 py-1 text-xs font-semibold text-green-600",
                    ),
                    class_name="flex items-center justify-between",
                ),
                class_name="flex items-start justify-between",
            ),
            rx.el.div(
                rx.el.p(
                    "REFLEX 应用",
                    class_name="mb-3 text-xs font-bold uppercase tracking-[0.2em] text-blue-600",
                ),
                rx.el.h1(
                    "Hello, Reflex!",
                    class_name="mb-4 text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl",
                ),
                rx.el.p(
                    "欢迎来到你的第一个 Reflex 应用。",
                    class_name="text-base leading-7 text-gray-600 sm:text-lg",
                ),
                rx.el.p(
                    "轻盈、清晰，从这里开始构建精彩体验。",
                    class_name="mt-1 text-sm leading-6 text-gray-500",
                ),
                class_name="mt-10",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("zap", class_name="h-4 w-4 text-blue-600"),
                    rx.el.span(
                        "一切准备就绪",
                        class_name="text-sm font-medium text-gray-700",
                    ),
                    class_name="flex items-center gap-2",
                ),
                rx.el.div(
                    rx.el.span(
                        "本地运行",
                        class_name="text-xs font-medium text-gray-400",
                    ),
                    rx.icon(
                        "arrow-up-right", class_name="h-4 w-4 text-gray-400"
                    ),
                    class_name="flex items-center gap-1",
                ),
                class_name="mt-10 flex items-center justify-between border-t border-gray-100 pt-5",
            ),
            class_name="w-full max-w-xl rounded-3xl border border-gray-200 bg-white p-7 sm:p-10",
        ),
        class_name="flex min-h-screen items-center justify-center bg-gray-50 px-5 py-12 font-sans",
    )


app = rx.App(theme=rx.theme(appearance="light"))
app.add_page(index, route="/")
