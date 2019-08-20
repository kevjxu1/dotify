from PIL import Image
import math

def fitToFrame(image, frameHeight, frameWidth):
    """Shrink image to fit in frame of given height and width, preserving the orignal aspect ratio"""
    w, h = image.size
    scale = min(frameWidth / w, frameHeight / h)
    if scale < 1:
        return image.resize((int(scale * w), int(scale * h)))
    else:
        return image


def computeBlock(pixels, startY, endY, startX, endX, thresh):

    def countPassedPixels(startY, endY, startX, endX, thresh):
        count = 0
        for y in range(startY, endY):
            for x in range(startX, endX):
                if pixels[x, y] > thresh:
                    count += 1

        return count

    block = [ [ 0, 0 ] for r in range(4) ]
    height, width = endY - startY, endX - startX
    strideY = int(math.ceil(height / 4))
    strideX = int(math.ceil(width / 2))
    countThresh = height * width / 16  # (height / 4) * (width / 2) / 2
    for y in range(4):
        for x in range(2):
            y0, x0 = startY + strideY * y, startX + strideX * x
            y1, x1 = min(endY, y0 + strideY), min(endX, x0 + strideX)
            count = countPassedPixels(y0, y1, x0, x1, thresh)
            if count >= countThresh:
                block[y][x] = 1
            else:
                block[y][x] = 0

    return block

def blockToBraille(block):
    """braille unicode characters are 0x2800 - 0x28FF
       @param block - 4x2 binary matrix"""
    h1 = block[1][1] | (block[2][1] << 1) | (block[3][0] << 2) | (block[3][1] << 3)
    h0 = block[0][0] | (block[1][0] << 1) | (block[2][0] << 2) | (block[0][1] << 3)
    offset = h0 | (h1 << 4)
    return chr(0x2800 + offset)


if __name__ == '__main__':
    thresh = 135
    outH, outW = 20, 40
    image = Image.open('test/pikachu.png')

    #if image.size[0] > 200 and image.size[1] > 200:
    #    image = image.resize((200, 200))
    #image = fitToFrame(image, 200, 200)
    image = image.convert('L')
    image = image.point(lambda p: 255 if p >= thresh else 0)
    image.save('test.jpg')
    w, h = image.size
    pixels = image.load()
    blockH = int(math.ceil(h / outH))
    blockW = int(math.ceil(w / outW))

    result = [ [ '\u2800' for x in range(outW) ] for y in range(outH) ]
    for y in range(outH):
        for x in range(outW):
            y0, x0 = y * blockH, x * blockW
            y1, x1 = min(h, y0 + blockH), min(w, x0 + blockW)
            block = computeBlock(pixels, y0, y1, x0, x1, thresh)
            char = blockToBraille(block)
            result[y][x] = char

    for x in range(len(result)):
        print(str.join('', result[x]))

    #strideX = 5
    #strideY = 10
    #result = []
    #for y in range(0, h, strideY):
    #    row = []
    #    for x in range(0, w, strideX):
    #        count = 0
    #        for yy in range(y, min(h, y + strideY)):
    #            for xx in range(x, min(w, x + strideX)):
    #                count += 0 if pixels[xx, yy] >= thresh else 1

    #        if count >= strideY * strideX / 2:
    #            row.append('\u28FF')
    #        else:
    #            row.append('\u2800')
    #    result.append(row)

    #for row in result:
    #    print(str.join('', row))

