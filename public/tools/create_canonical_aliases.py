import os
import shutil

ROOT = os.path.join(os.path.dirname(__file__), '..')

MAPPING = {
    'investor-resources-hub.html': 'resources.html',
    'what-results-means.html': 'results.html',
    'we-back-our-service-if-we-dont-deliver-youre-covered.html': 'guarantee.html',
    'the-unfair-advantage-for-modern-investors.html': 'advantage.html',
    'nationwide-sourcing.html': 'sourcing.html',
    'were-redefining-property-investment-by-making-it-simpler-more-transparent-and-less-stressful.html': 'about.html',
    'we-build-wealth-backed-by-15-years-of-experience.html': 'team.html',
}

def main():
    created = []
    for src, dst in MAPPING.items():
        src_path = os.path.join(ROOT, src)
        dst_path = os.path.join(ROOT, dst)
        if not os.path.isfile(src_path):
            print('Skipping; source missing:', src)
            continue
        # Only create if not already present
        if not os.path.isfile(dst_path):
            shutil.copyfile(src_path, dst_path)
            created.append(dst)
    print('Created', len(created), 'canonical aliases:')
    for f in created:
        print('-', f)

if __name__ == '__main__':
    main()

