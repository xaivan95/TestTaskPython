import random
from typing import List, Dict


class VersionGenerator:

    def __init__(self):
        self.generated_versions = set()

    def generate_versions_from_templates(self, templates: Dict[str, str]) -> Dict[str, List[str]]:
        results = {}

        for template_name, template in templates.items():
            versions = self._generate_template_versions(template, 2)
            results[template_name] = versions

        return results

    def _generate_template_versions(self, template: str, count: int = 2) -> List[str]:
        versions = []

        base_seed = hash(template) % 100

        for i in range(count):
            version = self._generate_single_version(template, base_seed + i, i)

            attempts = 0
            while version in self.generated_versions and attempts < 10:
                version = self._generate_single_version(
                    template,
                    base_seed + i + attempts + 20,
                    i
                )
                attempts += 1

            if version not in self.generated_versions:
                self.generated_versions.add(version)
                versions.append(version)

        return versions

    def _generate_single_version(self, template: str, seed: int, variant: int) -> str:
        parts = template.split('.')
        result_parts = []

        if seed is not None:
            random.seed(seed)

        for i, part in enumerate(parts):
            if part == '*':
                # TODO Когда-нибудь в каждом варианте будет свой подход к генерации
                if variant == 0:
                    number = (i + 1) % 10
                    if number == 0:
                        number = 1
                    result_parts.append(str(number))
                else:
                    number = random.randint(1, 9)
                    result_parts.append(str(number))
            else:
                result_parts.append(part)

        random.seed()

        return '.'.join(result_parts)

    def _generate_with_smart_strategy(self, template: str, variant: int) -> str:
        parts = template.split('.')
        #TODO Когда-нибудь тут будет выбираться различный подход к генерации
        strategies = [
            self._strategy_sequential,
            self._strategy_random_small,
            self._strategy_position_based,
            self._strategy_minimal,
        ]

        strategy = strategies[variant % len(strategies)]
        return strategy(parts)

    def _strategy_sequential(self, parts: List[str]) -> str:
        result_parts = []
        position = 1

        for part in parts:
            if part == '*':
                result_parts.append(str(position))
                position += 1
                if position > 9:
                    position = 1
            else:
                result_parts.append(part)

        return '.'.join(result_parts)

    def _strategy_random_small(self, parts: List[str]) -> str:
        result_parts = []

        for part in parts:
            if part == '*':
                result_parts.append(str(random.randint(1, 9)))
            else:
                result_parts.append(part)

        return '.'.join(result_parts)

    def _strategy_position_based(self, parts: List[str]) -> str:
        result_parts = []

        for i, part in enumerate(parts):
            if part == '*':
                if i == 0:
                    result_parts.append(str((i % 2) + 1))
                elif i == 1:
                    result_parts.append(str((i % 6)))
                else:
                    result_parts.append(str(random.randint(0, 9)))
            else:
                result_parts.append(part)

        return '.'.join(result_parts)

    def _strategy_minimal(self, parts: List[str]) -> str:
        result_parts = []

        for i, part in enumerate(parts):
            if part == '*':
                if i == 0:
                    result_parts.append('1')
                else:
                    result_parts.append('0')
            else:
                result_parts.append(part)

        return '.'.join(result_parts)