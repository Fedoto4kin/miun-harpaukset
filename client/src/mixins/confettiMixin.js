import confetti from 'canvas-confetti';

export const confettiMixin = {
    methods: {
        launchConfetti() {
            const count = 200;
            const defaults = {
                origin: { y: 0.7 },
            };

            function fire(particleRatio, opts) {
                confetti(
                    Object.assign({}, defaults, opts, {
                        particleCount: Math.floor(count * particleRatio),
                    })
                );
            }

            fire(0.25, {
                spread: 26,
                startVelocity: 55,
            });

            fire(0.2, {
                spread: 60,
            });

            fire(0.35, {
                spread: 100,
                decay: 0.91,
                scalar: 0.8,
            });

            fire(0.1, {
                spread: 120,
                startVelocity: 25,
                decay: 0.92,
                scalar: 1.2,
            });

            fire(0.1, {
                spread: 120,
                startVelocity: 45,
            });

            // Настройки для звездочек
            const star_defaults = {
                spread: 360,
                ticks: 50,
                gravity: 0,
                decay: 0.94,
                startVelocity: 30,
                shapes: ["star"],
                colors: ["FFE400", "FFBD00", "E89400", "FFCA6C", "FDFFB8"],
            };

            function shoot() {
                confetti({
                    ...star_defaults,
                    particleCount: 40,
                    scalar: 1.2,
                    shapes: ["star"],
                });

                confetti({
                    ...star_defaults,
                    particleCount: 10,
                    scalar: 0.75,
                    shapes: ["circle"],
                });
            }

            setTimeout(shoot, 0);
            setTimeout(shoot, 100);
            setTimeout(shoot, 200);
        },
    },
};
