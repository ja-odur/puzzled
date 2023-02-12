import hashlib
import re
from django.core.mail.message import EmailMessage, EmailMultiAlternatives
from django.template import engines, loader
import premailer


def email_to_dict(email_message):
    """
    Converts the specified email message to a dictionary representation.
    """
    if type(email_message) not in [EmailMessage, EmailMultiAlternatives]:
        return email_message
    email_message_data = {
        'subject': email_message.subject,
        'body': email_message.body,
        'from_email': email_message.from_email,
        'to': email_message.to,
        'bcc': email_message.bcc,
        'attachments': email_message.attachments,
        'headers': email_message.extra_headers,
        'cc': None,
        'reply_to': None,
    }
    if isinstance(email_message, EmailMultiAlternatives):
        email_message_data['alternatives'] = email_message.alternatives
    return email_message_data


def email_from_dict(email_message_data):
    """
    Creates an EmailMessage or EmailMultiAlternatives instance from the
    specified dictionary.
    """
    kwargs = dict(email_message_data)
    alternatives = kwargs.pop('alternatives', None)
    return (
        EmailMessage(**kwargs)
        if not alternatives
        else EmailMultiAlternatives(alternatives=alternatives, **kwargs)
    )


def get_html_text_template_pair(template_name):
    """
    Given a template_name returns the names of the text and html templates
    """
    html_template = 'html/{}.html'.format(template_name)
    text_template = 'text/{}.txt'.format(template_name)

    return html_template, text_template


def inline_styles(contents):
    if contents is None:
        return None

    if contents.strip():
        # Before passing this to premailer, make sure to rid the email from
        # any "special" characters, like all of our template variable
        # placeholders.  We'll scan the contents for any template variables or
        # control blocks, and replace their contents with their SHA1 hash.
        # Then, we apply premailer's inlining, after which we perform the
        # reverse replacement of the template variables.  This avoids
        # situations where premailer chokes on our template variables, e.g.
        # when they're inside an attribute value.
        blocks_re = re.compile(r'\{\%(.*?)\%\}')
        variable_re = re.compile(r'\{\{(.*?)\}\}')

        replacements = {}

        def hashit(matchobj):
            var_expr = matchobj.group(0)
            sha1 = '__{}__'.format(hashlib.sha1(var_expr).hexdigest())  # nosec
            replacements[sha1] = var_expr
            return sha1

        contents = blocks_re.sub(hashit, contents)
        contents = variable_re.sub(hashit, contents)

        # We are using Premailer for our CSS/HTML transformer
        transformer = premailer.Premailer(html=contents)

        # inline all styles
        contents = transformer.transform(encoding='ascii')

        for sha1, value in replacements.items():
            contents = contents.replace(sha1, value)

    return contents


def render_template(template_name, context=None, double_render=True):
    """Renders a template from the given name"""

    # Get Template object from given template_name
    html_template_name, text_template_name = get_html_text_template_pair(template_name)
    template = loader.get_template(html_template_name)  # jinja2 Template
    template_text = loader.render_to_string(text_template_name, context, using='jinja2')

    # Render Template -> String
    rendered_template_string = template.template.render()

    # Load string as Template then re-render now {% raw %} blocks are gone
    if double_render:
        engine = engines['jinja2']
        template = engine.from_string(rendered_template_string)
        rendered_template = template.render(context=context)
    else:
        rendered_template = rendered_template_string

    # Tidy up output
    rendered_template = inline_styles(rendered_template)

    return rendered_template, template_text
