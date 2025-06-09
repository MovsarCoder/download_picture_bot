



class CheckAdminDecorator:
    def __init__(self, func, callback_or_message, admin_users_list):
        self.callback_or_message = callback_or_message
        self.admin_users_list = admin_users_list
        self.func = func

    async def __call__(self, *args, **kwargs):
        if self.callback_or_message.from_user.id in self.admin_users_list:
            self.func(*args, **kwargs)

        else:
            await self.callback_or_message.answer(
                f'⚠️{self.callback_or_message.from_user.full_name}({self.callback_or_message.from_user.id}) вы не можете получить доступ к Admin функциям данного бота! Так как не являетесь Admin!')

