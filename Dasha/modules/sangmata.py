from pyrogram import filters
from pyrogram.types import Message
from Dasha.vars import COMMAND_HANDLER

from Dasha.ex_plugins.dbfunctions import (
    add_userdata,
    cek_userdata,
    get_userdata,
    is_sangmata_on,
    sangmata_off,
    sangmata_on,
)
from Dasha import pbot as app
from Dasha.modules.helper_funcs.chat_status import (
    is_user_ban_protected,
    user_admin,
)
from Dasha.modules.helper_funcs.handlers import MessageHandlerChecker
from Dasha.modules.helper_funcs.string_handling import (
    escape_invalid_curly_brackets,
    markdown_parser,
)
__mod__ = "SangMata"
__HELP__ = """"
This feature inspired from SangMata Bot. I'm created simple detection to check user data include username, first_name, and last_name.
/sangmata_set [on/off] - Enable/disable sangmata in groups.
"""


# Check user that change first_name, last_name and usernaname
@app.on_message(
    filters.group & ~filters.bot & ~filters.via_bot,
    group=5,
)
async def cek_mataa(_, ctx: Message):
    if ctx.sender_chat or not await is_sangmata_on(ctx.chat.id):
        return
    if not await cek_userdata(ctx.from_user.id):
        return await add_userdata(
            ctx.from_user.id,
            ctx.from_user.username,
            ctx.from_user.first_name,
            ctx.from_user.last_name,
        )
    usernamebefore, first_name, lastname_before = await get_userdata(ctx.from_user.id)
    msg = ""
    if (
        usernamebefore != ctx.from_user.username
        or first_name != ctx.from_user.first_name
        or lastname_before != ctx.from_user.last_name
    ):
        msg += f"👀 <b>Mata MissKaty</b>\n\n🌞 User: {ctx.from_user.mention} [<code>{ctx.from_user.id}</code>]\n"
    if usernamebefore != ctx.from_user.username:
        usernamebefore = f"@{usernamebefore}" if usernamebefore else strings("no_uname")
        usernameafter = (
            f"@{ctx.from_user.username}"
            if ctx.from_user.username
            else strings("no_uname")
        )
        msg += strings("uname_change_msg").format(bef=usernamebefore, aft=usernameafter)
        await add_userdata(
            ctx.from_user.id,
            ctx.from_user.username,
            ctx.from_user.first_name,
            ctx.from_user.last_name,
        )
    if first_name != ctx.from_user.first_name:
        msg += strings("firstname_change_msg").format(
            bef=first_name, aft=ctx.from_user.first_name
        )
        await add_userdata(
            ctx.from_user.id,
            ctx.from_user.username,
            ctx.from_user.first_name,
            ctx.from_user.last_name,
        )
    if lastname_before != ctx.from_user.last_name:
        lastname_before = lastname_before or strings("no_last_name")
        lastname_after = ctx.from_user.last_name or strings("no_last_name")
        msg += strings("lastname_change_msg").format(
            bef=lastname_before, aft=lastname_after
        )
        await add_userdata(
            ctx.from_user.id,
            ctx.from_user.username,
            ctx.from_user.first_name,
            ctx.from_user.last_name,
        )
    if msg != "":
        await ctx.reply_msg(msg, quote=False)


@app.on_message(filters.command("sangmata_set"))

@user_admin
async def set_mataa(_, ctx: Message, strings):
    if len(ctx.command) == 1:
        return await ctx.reply_msg(
            strings("set_sangmata_help").format(cmd=ctx.command[0]), del_in=6
        )
    if ctx.command[1] == "on":
        cekset = await is_sangmata_on(ctx.chat.id)
        if cekset:
            await ctx.reply_msg(strings("sangmata_already_on"))
        else:
            await sangmata_on(ctx.chat.id)
            await ctx.reply_msg(strings("sangmata_enabled"))
    elif ctx.command[1] == "off":
        cekset = await is_sangmata_on(ctx.chat.id)
        if not cekset:
            await ctx.reply_msg(strings("sangmata_already_off"))
        else:
            await sangmata_off(ctx.chat.id)
            await ctx.reply_msg(strings("sangmata_disabled"))
    else:
        await ctx.reply_msg(strings("wrong_param"), del_in=6)


