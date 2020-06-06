import apiai
import json
import uuid


def process_turn_full(utterance=None, debug=False, sid=None):
    if utterance is None:
        # peticion de inicio del dialogo
        request = ai.event_request(apiai.events.Event("WELCOME"))
        request.lang = 'es'
    elif len(utterance) == 0:
        return None, False, False
    else:
        request = ai.text_request()
        request.query = utterance
        request.session_id = sid
    response = json.loads(request.getresponse().read().decode('utf8'))
    # process
    if debug:
        print(json.dumps(response, indent=4))
        print(response.keys())
    contexts = response['result']['contexts']
    if len(contexts) > 0 and debug:
        print(list(c['name'] for c in contexts))
    answer = response['result']['fulfillment']['speech']
    all_filled = any(c['name'] == 'buy' for c in contexts)
    confirmed = any([c for c in contexts if c['name'] == 'confirmed'])
    canceled = any([c for c in contexts if c['name'] == 'canceled'])
    if debug and (all_filled or confirmed or canceled):
        print(json.dumps(response['result'], indent=4))
    return answer, confirmed, canceled


def process_turn_mini(utterance=None, sid=None):
    if utterance is None:
        # peticion de inicio del dialogo
        request = ai.event_request(apiai.events.Event("WELCOME"))
        request.lang = 'es'
    elif len(utterance) == 0:
        return None, False, False
    else:
        request = ai.text_request()
        request.query = utterance
        request.session_id = sid
    response = json.loads(request.getresponse().read().decode('utf8'))
    #  process
    answer = response['result']['fulfillment']['speech']
    contexts = [c['name'] for c in response['result']['contexts']]
    confirmed = 'confirmed' in contexts
    canceled = 'canceled' in contexts
    return answer, confirmed, canceled


def process_turn(utterance=None, debug=False, sid=None):
    if debug is False:
        return process_turn_mini(utterance, sid)
    else:
        return process_turn_full(utterance, True, sid)


if __name__ == "__main__":
    session_id = uuid.uuid4().hex
    CLIENT_ACCESS_TOKEN = "8e13c0d7e33a4fb5a7c36ef281865941"
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

    end = False
    user_turn = None
    while not end:
        if user_turn is not None and len(user_turn) > 0:
            print("User:", user_turn)
        utterance, end, begin = process_turn(
            utterance=user_turn, sid=session_id, debug=False)
        print("System:", utterance)
        if end:
            print('System: Gracias por utilizar nuestro servicio')
            break
        elif begin:
            user_turn = None
        else:
            user_turn = input('-->:')
