class MyBigInt:
    def __init__(self):
        self.data = []

    def set_hex(self, hex_str):
        self.data = []
        for i in range(0, len(hex_str), 8):
            chunk = hex_str[i:i + 8]
            self.data.append(int(chunk, 16))

    def get_hex(self):
        return self.__str__()

    def xor(self, other):
        result = MyBigInt()
        for i in range(max(len(self.data), len(other.data))):
            num1 = self.data[i] if i < len(self.data) else 0
            num2 = other.data[i] if i < len(other.data) else 0
            result.data.append(self.data[i] ^ other.data[i])
        return result

    def or_op(self, other):
        result = MyBigInt()
        for i in range(max(len(self.data), len(other.data))):
            num1 = self.data[i] if i < len(self.data) else 0
            num2 = other.data[i] if i < len(other.data) else 0
            result.data.append(num1 | num2)
        return result

    def and_op(self, other):
        result = MyBigInt()
        for i in range(max(len(self.data), len(other.data))):
            num1 = self.data[i] if i < len(self.data) else 0
            num2 = other.data[i] if i < len(other.data) else 0
            result.data.append(num1 & num2)
        return result

    def invert(self):
        inverted = []
        for i in self.data:
            inverted_num = ~i & 0xFFFFFFFF
            inverted.append(inverted_num)
        result = MyBigInt()
        result.data = inverted
        return result

    def shift_right(self, n):
        blocks = n // 32
        block_shift = n % 32
        result = MyBigInt()
        result.data = self.data.copy()
        result.data = result.data[blocks:]
        if block_shift > 0 and len(result.data) > 0:
            last_block = result.data[-1]
            preserved_bits = 32 - block_shift
            result.data[-1] = last_block >> block_shift
            result.data[-1] &= (1 << preserved_bits) - 1
        return result

    def shift_left(self, n):
        blocks = n // 32
        block_shift = n % 32
        result = MyBigInt()
        result.data = self.data.copy()
        for i in range(len(self.data)):
            result.data[i] <<= block_shift
            if i < len(result.data) - 1:
                result.data[i + 1] |= (result.data[i] >> 32)
        if blocks > 0:
            result.data.extend([0] * blocks)
        return result

    def add(self, other):
        max_len = max(len(self.data), len(other.data))
        self_data = [0] * (max_len - len(self.data)) + self.data[:]
        other_data = [0] * (max_len - len(other.data)) + other.data[:]
        result = []
        carry = 0
        for i in range(max_len - 1, -1, -1):
            digit_sum = self_data[i] + other_data[i] + carry
            result.append(digit_sum & 0xFFFFFFFF)  # Залишаємо тільки 32 молодших біта
            carry = digit_sum >> 32
        if carry != 0:
            result.append(carry)
            result.reverse()
            res = MyBigInt()
            res.data = result
        return result


    def subtract(self, other):
        result = MyBigInt()
        result.data = self.data[:]
        if len(other.data) >= len(self.data):
            for i in range(len(self.data)):
                result.data[i] -= other.data[i]
                if result.data[i] < 0:
                    j = i + 1
                    while j < len(result.data) and result.data[j] == 0:
                        j += 1
                    if j == len(result.data):
                        print("Negative result")
                    result.data[j] -= 1
                    for k in range(i + 1, j):
                        result.data[k] = 0xFFFFFFFF
                    result.data[i] += 0x100000000
        else:
            print("Negative result")

        # Remove leading zeros
        while len(result.data) > 1 and result.data[-1] == 0:
            result.data.pop()

        return result

    def modulo(self, modulus):
        mod_len = len(hex(modulus)[2:])
        num_len = len(self.data)
        if num_len < mod_len:
            return self
        remainder = MyBigInt()
        temp = MyBigInt()
        for i in range(num_len):
            temp.data.append(self.data[i])
            if len(temp.data) == mod_len:
                quotient = MyBigInt()
                div = 0
                for j in range(mod_len - 1, -1, -1):
                    div = (div << 32) | temp.data[j]
                    quotient.data.insert(0, div // modulus)
                    div %= modulus
                remainder.data.insert(0, div)
                temp.data = []
        if len(temp.data) > 0:
            remainder.data = temp.data
        return remainder

    def __str__(self):
        hex_str = ""
        for num in self.data:
            hex_str += format(num, "08x")
        return hex_str


numberA = MyBigInt()
numberB = MyBigInt()
numberA.set_hex("33ced2c76b26cae94e162c4c0d2c0ff7c13094b0185a3c122e732d5ba77efebc")
numberB.set_hex("22e962951cb6cd2ce279ab0e2095825c141d48ef3ca9dabf253e38760b57fe03")
print("Data type: " + str(type(numberA)))
print("A: " + numberA.get_hex())
print("A + B: " + str(numberA.add(numberB)))
print("A - B: " + str(numberA.subtract(numberB)))
print("A % 10: " + str(numberA.modulo(10)))
print("A XOR B: " + str(numberA.xor(numberB)))
print("INV A: " + str(numberA.invert()))
print("A OR B: " + str(numberA.or_op(numberB)))
print("A AND B: " + str(numberA.and_op(numberB)))
print("A shift 4 bits right: " + str(numberA.shift_right(4)))
print("A shift 4 bits left: " + str(numberA.shift_left(4)))
