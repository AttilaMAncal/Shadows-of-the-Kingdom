class HUD:
    def __init__(self, heart_img, coin_img, font):
        self.heart_img = heart_img
        self.coin_img = coin_img
        self.font = font

    def draw(self, screen, health, coin_count, elapsed_time):
        #kreslenie srdca
        for i in range(health):
            x = 10 + i * (self.heart_img.get_width() + 5)
            y = 10
            screen.blit(self.heart_img, (x, y))

        #počítadlo mincí
        x = 10
        y = 10 + self.heart_img.get_height() + 10
        screen.blit(self.coin_img, (x, y))
        text = self.font.render("x " + str(coin_count), True, (255, 255, 255))
        text_x = x + self.coin_img.get_width() + 5
        text_y = y + (self.coin_img.get_height() - text.get_height()) // 2
        screen.blit(text, (text_x, text_y))

        #timer
        time_y = y + self.coin_img.get_height() + 10
        time_text = self.font.render("Time: {:.2f}s".format(elapsed_time), True, (255, 255, 255))
        screen.blit(time_text, (10, time_y))
