def make_response_message(message, code, msg_key='msg'):
    return {
               'message': {
                   msg_key: message
               }
           }, code
