from decimal import Decimal


def format_number(value):
    if value is None:
        value = 0
    elif isinstance(value, Decimal):
        value = int(value * 10 ** 6)
    elif isinstance(value, float):
        raise ValueError('Please use decimal instead of float')
    return str(value)


class ContentMixin:

    def operation(self, content):
        return content

    def endorsement(self, level: int):
        """
        Endorse a block
        :param level: Endorsed level
        :return: Operation content
        """
        return self.operation({
            'kind': 'endorsement',
            'level': level
        })

    def seed_nonce_revelation(self, level: int, nonce):
        """
        Reveal the nonce committed operation in the previous cycle.
        More info https://tezos.stackexchange.com/questions/567/what-are-nonce-revelations
        :param level: When nonce hash was committed
        :param nonce: Hex string
        :return: Operation content
        """
        return self.operation({
            'kind': 'seed_nonce_revelation',
            'level': level,
            'nonce': nonce
        })

    def double_endorsement_evidence(self, op1: dict, op2: dict):
        """
        Provide evidence of double endorsement (endorsing two different blocks at the same block height).
        :param op1: Inline endorsement {
            "branch": $block_hash,
            "operations": {
                "kind": "endorsement",
                "level": integer ∈ [-2^31-2, 2^31+2]
            },
            "signature"?: $Signature
        }
        :param op2: Inline endorsement
        :return: Operation content
        """
        return self.operation({
            'kind': 'double_endorsement_evidence',
            'op1': op1,
            'op2': op2
        })

    def double_baking_evidence(self, bh1, bh2):
        """
        Provide evidence of double baking (two different blocks at the same height).
        :param bh1: First block hash
        :param bh2: Second block hash
        :return: Operation content
        """
        return self.operation({
            'kind': 'double_baking_evidence',
            'bh1': bh1,
            'bh2': bh2
        })

    def activate_account(self, activation_code, pkh=None):
        """
        Activate recommended allocations for contributions to the TF fundraiser.
        More info https://activate.tezos.com/
        :param pkh: Public key hash
        :param activation_code: Secret code from pdf
        :return: Operation content
        """
        return self.operation({
            'kind': 'activate_account',
            'pkh': pkh or '',
            'secret': activation_code
        })

    def proposals(self, proposals,
                  source=None, period=None):
        """
        Submit and/or upvote proposals to amend the protocol.
        Can only be submitted during a proposal period.
        More info https://tezos.gitlab.io/master/whitedoc/voting.html
        :param proposals: List of proposal hashes or single proposal hash
        :param source: Public key hash (of the signatory), leave none for autocomplete
        :param period: Number of the current voting period, leave none for autocomplete
        :return: Operation content
        """
        if not isinstance(proposals, list):
            proposals = [proposals]

        return self.operation({
            'kind': 'proposals',
            'source': source,
            'period': period,
            'proposals': proposals
        })

    def ballot(self, proposal, ballot,
               source=None, period=None):
        """
        Vote for a proposal in a given voting period.
        Can only be submitted during Testing_vote or Promotion_vote periods, and only once per period.
        More info https://tezos.gitlab.io/master/whitedoc/voting.html
        :param proposal: Hash of the proposal
        :param ballot: 'Yay', 'Nay' or 'Pass'
        :param source: Public key hash (of the signatory), leave none for autocomplete
        :param period: Number of the current voting period, leave none for autocomplete
        :return:
        """
        return self.operation({
            'kind': 'ballot',
            'source': source,
            'period': period,
            'proposal': proposal,
            'ballot': ballot
        })

    def reveal(self, public_key,
               source=None, counter=None, fee=None, gas_limit=None, storage_limit=None):
        """
        Reveal the public key associated with a tz address.
        :param public_key: Public key to reveal, Base58 encoded
        :param source:
        :param counter: Current michelson counter, leave none for autocomplete
        (More info https://tezos.stackexchange.com/questions/632/how-counter-grows)
        :param fee: Leave none for autocomplete
        :param gas_limit: Leave none for autocomplete
        :param storage_limit: Leave none for autocomplete
        :return:
        """
        return self.operation({
            'kind': 'reveal',
            'source': source,
            'fee': fee,
            'counter': counter,
            'gas_limit': gas_limit,
            'storage_limit': storage_limit,
            'public_key': public_key
        })

    def transaction(self, destination, amount=0, parameters=None,
                    source=None, counter=None, fee=None, gas_limit=None, storage_limit=None):
        """
        Transfer tezzies to an account (implicit or originated).
        If the receiver is an originated account (KT1…), then optional parameters may be passed.
        :param source:
        :param destination:
        :param amount:
        :param counter:
        :param parameters:
        :param fee:
        :param gas_limit:
        :param storage_limit:
        :return: Operation content
        """
        return self.operation({
            'kind': 'transaction',
            'source': source or '',
            'fee': format_number(fee),
            'counter': format_number(counter),
            'gas_limit': format_number(gas_limit),
            'storage_limit': format_number(storage_limit),
            'amount': format_number(amount),
            'destination': destination,
            'parameters': parameters or {}
        })

    def origination(self, script=None, manager_pubkey=None,
                    source=None, counter=None, fee=None, gas_limit=None, storage_limit=None):
        """
        :param manager_pubkey:
        :param script:
        :param source:
        :param counter:
        :param fee:
        :param gas_limit:
        :param storage_limit:
        :return:
        """
        return self.operation({
            'kind': 'transaction',
            'source': source,
            'fee': fee,
            'counter': counter,
            'gas_limit': gas_limit,
            'storage_limit': storage_limit,
            'manager_pubkey': manager_pubkey,
            'balance': 0,
            'script': script
        })

    def delegation(self, delegate=None,
                   source=None, counter=None, fee=None, gas_limit=None, storage_limit=None):
        """

        :param delegate:
        :param source:
        :param counter:
        :param fee:
        :param gas_limit:
        :param storage_limit:
        :return:
        """
        return self.operation({
            'kind': 'delegation',
            'source': source,
            'fee': fee,
            'counter': counter,
            'gas_limit': gas_limit,
            'storage_limit': storage_limit,
            'delegate': delegate
        })

#
# class Transaction(Content):
#
#     @classmethod
#     def build(cls, destination, amount: int, parameters=None,
#               source=None, counter=None, fee=None, gas_limit=None, storage_limit=None):
#         """
#         Transfer tezzies to an account (implicit or originated).
#         If the receiver is an originated account (KT1…), then optional parameters may be passed.
#         :param source:
#         :param destination:
#         :param amount:
#         :param counter:
#         :param parameters:
#         :param fee:
#         :param gas_limit:
#         :param storage_limit:
#         :return: Operation content
#         """
#         return {
#             'kind': 'transaction',
#             'source': source,
#             'fee': fee,
#             'counter': counter,
#             'gas_limit': gas_limit,
#             'storage_limit': storage_limit,
#             'amount': amount,
#             'destination': destination,
#             'parameters': parameters
#         }
#
#     @classmethod
#     def to_bytes(cls, content):
#         res = encode_int(operation_tags[content['kind']])
#         res += encode_address(content["source"])
#         res += encode_int(int(content["fee"]))
#         res += encode_int(int(content["counter"]))
#         res += encode_int(int(content["gas_limit"]))
#         res += encode_int(int(content["storage_limit"]))
#         res += encode_int(int(content["amount"]))
#         res += encode_address(content["destination"])
#
#         if content["parameters"]:
#             res += encode_boolean(True)
#             parameters = micheline_to_bytes(content["parameters"])
#             res += len(parameters).to_bytes(4, 'big') + parameters
#         else:
#             res += encode_boolean(False)
#
#         return res
