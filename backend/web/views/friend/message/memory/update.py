import logging
from pprint import pprint
from django.utils.timezone import now

from web.views.friend.message.memory.graph import MemoryGraph
from web.models.friend import Friend, Message, SystemPrompt

from langchain_core.messages import SystemMessage, HumanMessage

logger = logging.getLogger(__name__)


def create_system_msg() -> SystemMessage:
    system_message = SystemPrompt.objects.filter(title='记忆').order_by('order_number')
    prompt = ''
    for sp in system_message:
        prompt += sp.prompt
    return SystemMessage(prompt)

def create_human_msg(friend: Friend):
    prompt = f"【原始回忆】\n{friend.memory}\n"
    prompt += f"【最近对话】\n"
    messages = list(Message.objects.filter(friend=friend).order_by("-id")[:10])
    messages.reverse()
    for m in messages:
        prompt += f"user: {m.user_message}\n"
        prompt += f"ai: {m.output}\n"
    return HumanMessage(prompt)

def update_memory(friend: Friend):
    app = MemoryGraph.create_app()

    inputs = {
        'messages' : [
            create_system_msg(),
            create_human_msg(friend),
        ]
    }

    pprint(inputs)
    r = app.invoke(inputs)
    content = r.get("messages")[-1].content

    try:
        friend.memory = content
    except Exception:
        logger.exception("failed to parse memory JSON, keeping previous memory: %s", content)
        return

    pprint(friend.memory)

    friend.updated_at = now()
    friend.save()